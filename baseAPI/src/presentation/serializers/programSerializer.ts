import type { IProgram } from '@/models/index'
import type { IProgramGroupWithPrograms } from '@/services/programGroupService'

export function serializeProgram(program: IProgram) {
  return {
    id: program.id,
    name: program.name,
    description: program.description,
    path_to_executable_file: program.pathToExecutableFile,
    groupId: program.groupId
  }
}

export function serializeProgramGroup(group: IProgramGroupWithPrograms) {
  return {
    id: group.id,
    name: group.name,
    description: group.description,
    programs: group.programs.map(serializeProgram)
  }
}
