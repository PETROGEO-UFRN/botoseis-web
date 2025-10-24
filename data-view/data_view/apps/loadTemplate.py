from pathlib import Path
from jinja2 import Template

from ..constants import URL_PATHS


def __loadVariables(
    template: Template,
    variables: dict[str, str | bool]
):
    for key, value in variables.items():
        template.globals[key] = value


def loadTemplate(
    template_path: Path,
    template_variables: dict[str, str | bool]
) -> Template:
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
                # *** skip main template
                if key_name == template_path.stem:
                    continue

                with open(file_path, "r", encoding="utf-8") as partial_template_file:
                    partial_template = Template(partial_template_file.read())
                    __loadVariables(partial_template, template_variables)
                    rendered = partial_template.render(
                        STATIC_PATH=URL_PATHS.STATIC_FILES
                    )
                    html_template.globals[key_name] = rendered
                __loadVariables(html_template, template_variables)

        return html_template
