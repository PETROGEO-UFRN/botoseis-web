from pathlib import Path
from jinja2 import Template

from .paths import STATIC_URL_PATH


def loadTemplate(template_path: Path) -> Template:
    """
    Load a Jinja2 template.

    Add all other HTML files in the same folder as globals.

    The global can be used in the index html file by:

    {{ file_name }}

    {{ file_name | safe }}
    """

    template_module_folder = template_path.parent

    with open(template_path, "r", encoding="utf-8") as index_template_file:
        html_template = Template(index_template_file.read())

        # *** Search for aditional files in the HTML file folder
        for file_path in template_module_folder.iterdir():
            if file_path.is_file() and file_path.suffix == ".html":
                key_name = file_path.stem
                # *** skip main template itself
                if key_name == template_path.stem:
                    continue

                with open(file_path, "r", encoding="utf-8") as partial_template_file:
                    partial_template = Template(partial_template_file.read())
                    rendered = partial_template.render(
                        STATIC_PATH=STATIC_URL_PATH
                    )
                    html_template.globals[key_name] = rendered
                html_template.globals["STATIC_PATH"] = STATIC_URL_PATH

        return html_template
