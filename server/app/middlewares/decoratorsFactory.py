from typing import Callable

# *** This factory is necessery mainly to avoid
# *** "existing endpoint function" error with flask routers


def decorator_factory(
        decorator: Callable[[Callable], Callable],
        **factory_kwargs
) -> Callable[[Callable], any]:
    def modified_decorator(*args, **kwargs):
        decorated_function = decorator(*args, **kwargs, **factory_kwargs)
        decorated_function.__name__ = f"{id(decorated_function)}"
        return decorated_function
    return modified_decorator
