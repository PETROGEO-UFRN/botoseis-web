import logging
import json
import os

from .read_programs_docs import read_program_doc, jsonofy_sdoc

logging.basicConfig(level=logging.DEBUG, format="%(message)s")

programs_dir = "app/cli/su_programs"
home_dir = os.environ.get("HOME")
PROGRAMS_DIR = f"{home_dir}/SeismicUnix/src/su/main"

def write_programs_docs() -> None:
    os.makedirs(programs_dir, exist_ok=True)
    for folder_name in sorted(os.listdir(PROGRAMS_DIR)):
        if not os.path.isdir(os.path.join(PROGRAMS_DIR, folder_name)):
            continue
        data = {
            "count_programs": 0,
            "programGroups": []
        }

        logging.debug(f"Current group: {folder_name}")
        folder_path = os.path.join(PROGRAMS_DIR, folder_name)
        if os.path.isdir(folder_path):
            program_group = {
                "name": folder_name,
                "description": "",
                "programs": []
            }

            for file_name in sorted(os.listdir(folder_path)):
                if not file_name.endswith(".c"):
                    continue

                file_path = os.path.join(folder_path, file_name)
                try:
                    sdoc = read_program_doc(file_path)
                    program_db = jsonofy_sdoc(sdoc)
                except ValueError:
                    logging.debug(f"Value error for program: {file_name}")
                    continue
                except Exception as e:
                    logging.debug(f"\033[91mSome error occurred with program: {file_name}\033[0m")
                    logging.debug(e)
                    exit(1)

                if program_db:
                    program_group["programs"].append(program_db)

            if program_group["programs"]:
                data["programGroups"].append(program_group)
                data["count_programs"] += len(program_group["programs"])

        with open(os.path.join(programs_dir, f"{folder_name}.json"), "w") as f:
            json.dump(data, f, indent=4)
