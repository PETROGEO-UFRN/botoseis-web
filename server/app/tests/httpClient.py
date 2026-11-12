"""HTTP adapters that let the Flask-style test suite run against a real server.

``GenericHttpClient`` mimics ``flask.testing.FlaskClient`` (``get``, ``post``,
``put``, ``delete``, ``patch``, ``set_cookie``, ``delete_cookie``) on top of
``requests``. ``FlaskResponseAdapter`` mimics the Werkzeug test response
(``.data`` bytes, ``.json`` property, ``.status_code``, ``.headers``...).

Cookie handling follows ``werkzeug.test.Client`` on purpose:
  - one cookie per (domain, path, name); a response cookie replaces a
    cookie set with ``set_cookie`` under the same key.
  - the ``Secure`` flag is ignored, so ``JWT_COOKIE_SECURE`` cookies still
    travel over plain ``http://``.
  - stored cookies replace any ``Cookie`` header passed by the caller.
"""
import json as json_module
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from http.cookiejar import DefaultCookiePolicy
from http.cookies import SimpleCookie
from io import IOBase
from urllib.parse import urlsplit

import requests
from requests.structures import CaseInsensitiveDict

DEFAULT_TIMEOUT = 30


class _Cookie:
    def __init__(self, key, value, domain, path, origin_only=True):
        self.key = key
        self.value = value
        self.domain = domain
        self.path = path
        self.origin_only = origin_only

    @property
    def storage_key(self):
        return (self.domain, self.path, self.key)

    def matches(self, host, path):
        domain_ok = host == self.domain or (
            not self.origin_only
            and host.endswith(self.domain)
            and host[: -len(self.domain)].endswith(".")
        )
        path_ok = path == self.path or (
            path.startswith(self.path)
            and path[len(self.path) - self.path.endswith("/"):].startswith("/")
        )
        return domain_ok and path_ok


def _should_delete(morsel):
    max_age = morsel["max-age"]
    if max_age != "":
        try:
            return int(max_age) <= 0
        except ValueError:
            return False
    expires = morsel["expires"]
    if expires:
        try:
            return parsedate_to_datetime(expires) <= datetime.now(timezone.utc)
        except (TypeError, ValueError):
            return False
    return False


class _ResponseHeaders:
    """Read-only, multi-value, case-insensitive headers (werkzeug ``Headers``-like)."""

    def __init__(self, items):
        self._items = list(items)

    def getlist(self, key):
        key = key.lower()
        return [v for k, v in self._items if k.lower() == key]

    def get(self, key, default=None, type=None):
        values = self.getlist(key)
        if not values:
            return default
        if type is None:
            return values[0]
        try:
            return type(values[0])
        except ValueError:
            return default

    def __getitem__(self, key):
        values = self.getlist(key)
        if not values:
            raise KeyError(key)
        return values[0]

    def __contains__(self, key):
        return bool(self.getlist(key))

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return len(self._items)

    def items(self):
        return list(self._items)

    def keys(self):
        return [k for k, _ in self._items]

    def values(self):
        return [v for _, v in self._items]

    def __repr__(self):
        return f"{self.__class__.__name__}({self._items!r})"


class FlaskResponseAdapter:
    """Wraps ``requests.Response`` with the Flask/Werkzeug test response API."""

    def __init__(self, response: requests.Response):
        self._response = response
        raw_headers = getattr(response.raw, "headers", None)
        if raw_headers is not None and hasattr(raw_headers, "items"):
            self.headers = _ResponseHeaders(raw_headers.items())
        else:
            self.headers = _ResponseHeaders(response.headers.items())

    @property
    def status_code(self):
        return self._response.status_code

    @property
    def status(self):
        return f"{self._response.status_code} {self._response.reason or ''}".strip()

    @property
    def data(self) -> bytes:
        return self._response.content

    def get_data(self, as_text=False):
        return self.text if as_text else self.data

    @property
    def text(self):
        return self._response.text

    @property
    def content_type(self):
        return self.headers.get("Content-Type")

    @property
    def mimetype(self):
        content_type = self.content_type
        if not content_type:
            return None
        return content_type.split(";", 1)[0].strip().lower()

    @property
    def is_json(self):
        mimetype = self.mimetype
        return mimetype is not None and (
            mimetype == "application/json"
            or (mimetype.startswith("application/") and mimetype.endswith("+json"))
        )

    @property
    def json(self):
        return self.get_json()

    def get_json(self, force=False, silent=False):
        # *** Returns None unless the mimetype is JSON (werkzeug contract)
        if not (force or self.is_json):
            return None
        try:
            return json_module.loads(self.data)
        except ValueError:
            if not silent:
                raise
            return None

    @property
    def location(self):
        return self.headers.get("Location")

    def __getattr__(self, name):
        # *** Attributes not emulated are read from the underlying requests.Response
        return getattr(self._response, name)

    def __repr__(self):
        return f"<{self.__class__.__name__} {len(self.data)} bytes [{self.status}]>"


class GenericHttpClient:
    """Flask ``test_client()`` lookalike that sends real HTTP requests."""

    def __init__(self, base_url: str, timeout: float = DEFAULT_TIMEOUT):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()
        # *** Cookies are stored by this client (werkzeug semantics), not by requests
        self._session.cookies.set_policy(_RejectAllCookies())
        self._cookies: dict = {}
        self._host = urlsplit(self.base_url).hostname or "localhost"

    # *** HTTP verbs, same call shape as FlaskClient
    def get(self, path="/", **kwargs):
        return self.open(path, method="GET", **kwargs)

    def post(self, path="/", **kwargs):
        return self.open(path, method="POST", **kwargs)

    def put(self, path="/", **kwargs):
        return self.open(path, method="PUT", **kwargs)

    def delete(self, path="/", **kwargs):
        return self.open(path, method="DELETE", **kwargs)

    def patch(self, path="/", **kwargs):
        return self.open(path, method="PATCH", **kwargs)

    def head(self, path="/", **kwargs):
        return self.open(path, method="HEAD", **kwargs)

    def options(self, path="/", **kwargs):
        return self.open(path, method="OPTIONS", **kwargs)

    def open(
        self,
        path="/",
        method="GET",
        *,
        json=None,
        data=None,
        headers=None,
        content_type=None,
        query_string=None,
        follow_redirects=False,
        **_ignored,
    ):
        url = self._build_url(path)
        request_headers = self._normalize_headers(headers)
        request_kwargs = {}

        if json is not None:
            request_kwargs["json"] = json
        elif data is not None:
            form, files = self._split_form_data(data)
            if files is not None:
                request_kwargs["files"] = files
                if form:
                    request_kwargs["data"] = form
            else:
                request_kwargs["data"] = form

        is_multipart = "files" in request_kwargs
        if content_type and content_type.lower().startswith("multipart/form-data"):
            if data is not None and not is_multipart:
                # *** Force multipart encoding even without file fields
                request_kwargs["files"] = [
                    (key, (None, str(value)))
                    for key, value in self._iter_items(request_kwargs.pop("data") or {})
                ]
                is_multipart = True
        elif content_type:
            request_headers["Content-Type"] = content_type

        if is_multipart:
            # *** Content-Type is left to requests, which sets the multipart boundary
            request_headers.pop("Content-Type", None)

        request_path = urlsplit(url).path or "/"
        # *** Stored cookies replace a caller "Cookie" header (werkzeug behavior)
        request_headers.pop("Cookie", None)
        cookie_header = "; ".join(
            f"{c.key}={c.value}"
            for c in self._cookies.values()
            if c.matches(self._host, request_path)
        )
        if cookie_header:
            request_headers["Cookie"] = cookie_header

        response = self._session.request(
            method,
            url,
            params=query_string,
            headers=request_headers,
            allow_redirects=follow_redirects,
            timeout=self.timeout,
            **request_kwargs,
        )
        self._update_cookies(response, request_path)
        return FlaskResponseAdapter(response)

    # *** Cookie API, same signatures as werkzeug.test.Client
    def set_cookie(self, key, value="", *, domain=None, origin_only=True, path="/", **kwargs):
        cookie = _Cookie(key, value, domain or self._host, path, origin_only)
        self._cookies[cookie.storage_key] = cookie

    def delete_cookie(self, key, *, domain=None, path="/"):
        self._cookies.pop((domain or self._host, path, key), None)

    def get_cookie(self, key, domain=None, path="/"):
        return self._cookies.get((domain or self._host, path, key))

    def close(self):
        self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.close()

    # *** Internals
    def _build_url(self, path):
        if path.startswith(("http://", "https://")):
            return path
        return f"{self.base_url}/{path.lstrip('/')}"

    @staticmethod
    def _normalize_headers(headers):
        normalized = CaseInsensitiveDict()
        if headers is None:
            return normalized
        items = headers.items() if hasattr(headers, "items") else headers
        for key, value in items:
            normalized[key] = value
        return normalized

    @staticmethod
    def _iter_items(data):
        items = data.items() if hasattr(data, "items") else data
        for key, value in items:
            if isinstance(value, list):
                for item in value:
                    yield key, item
            else:
                yield key, value

    @classmethod
    def _split_form_data(cls, data):
        """Convert werkzeug-style ``data`` into requests ``data``/``files``.

        Werkzeug accepts file fields as a file object or a tuple of
        ``(file, filename[, content_type])``; requests expects
        ``(filename, file[, content_type])``.
        """
        if isinstance(data, (str, bytes, bytearray)) or not (
            hasattr(data, "items") or isinstance(data, (list, tuple))
        ):
            return data, None

        form, files = [], []
        for key, value in cls._iter_items(data):
            if isinstance(value, tuple) and value and cls._is_file(value[0]):
                file_obj = value[0]
                filename = value[1] if len(value) > 1 else cls._filename(file_obj)
                if len(value) > 2:
                    files.append((key, (filename, file_obj, value[2])))
                else:
                    files.append((key, (filename, file_obj)))
            elif cls._is_file(value):
                files.append((key, (cls._filename(value), value)))
            else:
                form.append((key, value))
        return form, (files or None)

    @staticmethod
    def _is_file(value):
        return isinstance(value, IOBase) or hasattr(value, "read")

    @staticmethod
    def _filename(file_obj):
        name = getattr(file_obj, "name", None)
        return name.replace("\\", "/").rsplit("/", 1)[-1] if isinstance(name, str) else None

    def _update_cookies(self, response, request_path):
        raw_headers = getattr(response.raw, "headers", None)
        if raw_headers is not None and hasattr(raw_headers, "getlist"):
            set_cookie_headers = raw_headers.getlist("Set-Cookie")
        else:
            value = response.headers.get("Set-Cookie")
            set_cookie_headers = [value] if value else []

        default_path = request_path.rpartition("/")[0] or "/"
        for header in set_cookie_headers:
            parsed = SimpleCookie()
            try:
                parsed.load(header)
            except Exception:
                continue
            for morsel in parsed.values():
                domain_attr = morsel["domain"].lstrip(".")
                cookie = _Cookie(
                    key=morsel.key,
                    # *** Raw (still encoded) value, as stored by werkzeug
                    value=header.split(";", 1)[0].partition("=")[2].strip(),
                    domain=domain_attr or self._host,
                    path=morsel["path"] or default_path,
                    origin_only=not domain_attr,
                )
                if _should_delete(morsel):
                    self._cookies.pop(cookie.storage_key, None)
                else:
                    self._cookies[cookie.storage_key] = cookie


class _RejectAllCookies(DefaultCookiePolicy):
    def set_ok(self, cookie, request):
        return False

    def return_ok(self, cookie, request):
        return False
