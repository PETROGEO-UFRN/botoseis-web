import re
from typing import Literal

def read_program_doc(program_path: str) -> list[str]:
    with open(program_path, "r") as f:
        content = f.read()

    doc_pattern = r'char\s*\*?\s*sdoc\s*\[\]?\s*=\s*\{(.*?)\};'

    match = re.search(doc_pattern, content, re.DOTALL)
    if not match:
        raise ValueError(f"No match for program: {program_path}")

    try:
        sdoc_content = match.group(1)
        lines = [line.replace('"', '')[:-1].strip() for line in sdoc_content.splitlines() if len(set(line)) > 3]
        lines = [line for line in lines if len(line) > 0] # Some how, I can only filter the size of the lines here
        return lines

    except Exception as e:
        raise Exception(f"Some error happened to read the doc of the file: {program_path}\nError: {e}")

def detect_type(value: str) -> Literal["integer", "float", "string"]:
    if value.isdigit():  # Only digits (e.g., "42")
        return "integer"
    elif re.match(r'^\d+\.\d+$', value):  # Digits with a dot (e.g., "3.14")
        return "float"
    else:  # Only letters or mixed (e.g., "hello", "param1")
        return "string"

def jsonofy_sdoc(sdoc_lines: list[str]) -> dict[str, str]:
    db_data = {
        "name": "",
        "description": "",
        "path_to_executable_file": "",
        "parameters": [],
    }

    try:
        db_data["name"] = db_data["path_to_executable_file"] = sdoc_lines[0].split()[0]
    except Exception as e:
        raise Exception(f"Error in extracting the sdco for sdoc: {sdoc_lines}\nError: {e}")

    # Check if description is on the same line or the next line
    if "-" in sdoc_lines[0]:
        db_data["description"] = sdoc_lines[0].split("-", 1)[1].strip()
    elif len(sdoc_lines) > 1 and sdoc_lines[1].strip() == "":
        db_data["description"] = sdoc_lines[2].strip() if len(sdoc_lines) > 2 else ""
    else:
        db_data["description"] = sdoc_lines[1].strip() if len(sdoc_lines) > 1 else ""

    # Get parameters
    isRequired = False
    for line in sdoc_lines:
        parameter_pattern = r'(\w+)=([\w,\.()]+)\s+(.*)'
        if "Required" in line:
            isRequired = True
        elif "Optional" in line:
            isRequired = False
        match = re.match(parameter_pattern, line)
        if match:
            input_type = detect_type(match.group(2))
            db_data["parameters"].append({
            "name": match.group(1),
            "description": match.group(3).strip(),
            "example": match.group(2),
            "input_type": input_type,
            "isRequired": isRequired,
        })

    return db_data
