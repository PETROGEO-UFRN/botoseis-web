// ! Duplicated ! Shall be shared from "admin" as well as its types
import type { Key } from 'react'

type parameterFileInputType = `file:${helperFileTypes}`

import { StaticTabKey } from 'constants/clientPrograms'

type clientGroupIdType = "client-side-programs"

declare global {
  type clientProgramIdType = Exclude<
    StaticTabKey,
    StaticTabKey.Input
  >

  interface IParameter {
    id: number
    name: string
    description: string
    input_type: "float" | "integer" | "string" | parameterFileInputType
    isRequired: boolean
  }

  type GenericProgramConstructorKeysType = "name" | "description" | "path_to_executable_file" | "groupId"
  interface IGenericProgramConstructor {
    name: string
    description: string
    path_to_executable_file: string
    groupId: number
  }

  interface IGenericProgram<
    ProgramIDType extends Key = number
  > extends IGenericProgramConstructor {
    id: ProgramIDType
    groupId: number | clientGroupIdType
    // parameters: Array<IParameter>
  }

  interface IProgramsGroupConstructor {
    name: string
    description: string
  }

  interface IProgramsGroup<
    ProgramIDType extends Key = number
  > extends IProgramsGroupConstructor {
    id: number | clientGroupIdType
    programs: Array<IGenericProgram<ProgramIDType>>
  }
}
