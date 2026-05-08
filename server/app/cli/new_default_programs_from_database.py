import json
from tqdm import tqdm

from ..models.ProgramGroupModel import ProgramGroupModel
from ..models.ProgramModel import ProgramModel
from ..models.ParameterModel import ParameterModel

from .get_CLI_dir_path import get_CLI_dir_path

def new_default_programs_from_database():
    groups_result = []
    count_groups = 0
    count_programs = 0
    print('Fetching database...')
    programGroups = ProgramGroupModel.query.all()
    max_programs = ProgramModel.query.count()

    progressBar = tqdm(total=max_programs, desc="Loading database programs...")

    for group in programGroups:
        count_programs += 1
        group_info = group.getAttributes()

        for program in group_info['programs']:
            count_programs += 1

            parameters = ParameterModel.query.filter_by(programId=program['id']).all()
            program['parameters'] = []
            for parameter in parameters:
                parameter_data = parameter.getAttributes()
                del parameter_data['id']
                program['parameters'].append(parameter_data)

            del program['id']
            del program['groupId']
            progressBar.update(1)
        del group_info['id']
        groups_result.append(group_info)

    with open(get_CLI_file_path(), 'w') as file: # Fix
        json.dump(
            {
                "count_programs": count_programs,
                "programGroups": groups_result
            },
            file,
            indent=2
        )
        print('Programs exported from database to JSON.')
        print('Including entities from this tables:')
        print(' - program_groups_table')
        print(' - programs_table')
        print(' - parameters_table')
        print(f'\nExported {count_programs} programs divided in {count_groups} groups')
