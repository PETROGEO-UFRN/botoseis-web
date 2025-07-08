import type { StaticTabKey } from 'constants/StaticTabKey'
// *** generic entities also represets "resumed" version of entities ***

declare global {
  interface IgenericTab {
    id: number | StaticTabKey
    name: string
    // ! is_active at a generic must be reviewed
    is_active?: boolean
  }

  type literals = Array<string>
  type primitevesTypes = string | number | boolean | Array<number> | literals | headers
  interface IgenericEntitiesType {
    id: number
    name: string
  }

  interface IProject extends IgenericEntitiesType {
    userId: string
    // !turn into isostring date type
    created_at: string
    modified_at: string
  }

  interface ILine extends IgenericEntitiesType {
    projectId: number
    workflows: Array<IResumedWorkflow>
  }

  interface IWorkflow extends IgenericEntitiesType {
    input_file_link_id: number
    output_name: string
    commands: Array<ICommand>
    parentType: 'dataset' | 'project' | 'line',
  }

  interface IResumedWorkflow extends IgenericEntitiesType {
  }

  interface ICommand extends IgenericTab {
    workflowId: number
    program_id: number
    is_active?: boolean
    // *** stringfied json, but currently [commit 7640f54] accepts any object
    parameters: string
  }

  type orderedCommandsListType = Array<ICommand>

  type idsType = Array<number>
}
