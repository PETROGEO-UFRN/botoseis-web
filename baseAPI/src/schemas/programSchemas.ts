import { createSelectSchema } from 'drizzle-zod'
import { z } from 'zod'

import { programGroups, programs } from '@/models/index'
import {
  AT_LEAST_ONE_FIELD,
  hasAnyField,
  optionalString,
  requestBody,
  requiredString
} from '@/schemas/commonSchemas'

export const ProgramSchema = createSelectSchema(programs)

// *** path_to_executable_file is a plain text field, uploads are not handled
export const ProgramCreateSchema = requestBody({
  name: requiredString(),
  description: requiredString(),
  path_to_executable_file: requiredString()
})

export const ProgramUpdateSchema = ProgramCreateSchema

export const ProgramResponseSchema = ProgramSchema.transform(program => ({
  id: program.id,
  name: program.name,
  description: program.description,
  path_to_executable_file: program.pathToExecutableFile,
  groupId: program.groupId
}))

export const ProgramGroupSchema = createSelectSchema(programGroups)

export const ProgramGroupWithProgramsSchema = ProgramGroupSchema.extend({
  programs: z.array(ProgramSchema)
})

export const ProgramGroupCreateSchema = requestBody({
  name: requiredString(),
  description: optionalString().optional()
})

export const ProgramGroupUpdateSchema = requestBody({
  name: optionalString().optional(),
  description: optionalString().optional()
}).refine(hasAnyField, { error: AT_LEAST_ONE_FIELD })

export const ProgramGroupResponseSchema = ProgramGroupWithProgramsSchema.extend(
  { programs: z.array(ProgramResponseSchema) }
)

export type IProgramData = z.infer<typeof ProgramCreateSchema>
export type IProgramGroupWithPrograms = z.infer<
  typeof ProgramGroupWithProgramsSchema
>
export type IProgramGroupCreate = z.infer<typeof ProgramGroupCreateSchema>
export type IProgramGroupUpdate = z.infer<typeof ProgramGroupUpdateSchema>
