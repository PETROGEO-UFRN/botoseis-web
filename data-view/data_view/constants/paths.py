from pathlib import Path

index_template_path = (
    Path(__file__).parent.parent / "templates" / "index.html"
).resolve()

static_url_path = "/public/"

static_files_path = (Path(__file__).parent.parent / "public").resolve()
