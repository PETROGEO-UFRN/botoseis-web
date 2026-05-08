import json
import os
from logging import warning
from tqdm import tqdm

from ..models.ProgramGroupModel import ProgramGroupModel
from ..models.ProgramModel import ProgramModel
from ..models.ParameterModel import ParameterModel
from ..database.connection import database

from .get_CLI_dir_path import get_CLI_dir_path

# *** This script will only be accepted for a table with no lines.
# *** Forcely run it on an alredy initialized database may lead
# *** to duplicated programs other issues.
def populate_database_programs():
    if ProgramModel.query.count() > 0:
        warning("Database alredy initialized. Can only populate empty tables")
        return None

    programs_dir = get_CLI_dir_path()
    for program_file in os.listdir(programs_dir):
        program_file_path = os.path.join(programs_dir, program_file)
        with open(program_file_path) as file:
            fileContent = json.loads(file.read())
            count_programs = fileContent["count_programs"]
            programGroups = fileContent["programGroups"]

            progressBar = tqdm(total=count_programs, desc="Posting programs into database...")

            # * Create default rows *
            # * "default_programs" are usually Seismic Unix programs *

            resultParameters = []

            for programGroupInfo in programGroups:
                createdProgramGroup = ProgramGroupModel(
                    name=programGroupInfo["name"],
                    description=programGroupInfo["description"],
                )
                database.session.add(createdProgramGroup)
                database.session.commit()

                for programInfo in programGroupInfo["programs"]:
                    createdProgram = ProgramModel(
                        name = programInfo["name"],
                        description = programInfo["description"],
                        path_to_executable_file = programInfo["path_to_executable_file"],
                        # *** createdProgramGroup shall have an ID by now
                        groupId = createdProgramGroup.id,
                    )
                    database.session.add(createdProgram)
                    database.session.commit()
                    for parameterInfo in programInfo["parameters"]:
                        # *** create Parameter by database level rules
                        createdParameter = ParameterModel(
                            name = parameterInfo["name"],
                            description = parameterInfo["description"],
                            input_type = parameterInfo["input_type"],
                            isRequired = parameterInfo["isRequired"],
                            # *** createdProgram shall have an ID by now
                            programId = createdProgram.id,
                        )
                        resultParameters.append(createdParameter)
                    # *** update progress bar for each program fully loaded
                    progressBar.update(1)

            # *** Insert parameters all at once
            database.session.bulk_save_objects(resultParameters)
            database.session.commit()
