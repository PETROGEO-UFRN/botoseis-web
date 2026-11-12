import { asc, eq } from 'drizzle-orm'

import database from '@/database/connection'
import { AppError } from '@/errors/AppError'
import { type IParameter, parameters } from '@/models/index'
import { PROGRAM_NOT_FOUND, programService } from '@/services/programService'

export const PARAMETER_NOT_FOUND = 'Parameter does not exist'

export interface IParameterUpdateData {
  name?: string
  description?: string
  example?: string
  input_type?: string
  isRequired?: boolean
}

export const parameterService = {
  async listByProgramId(programId: number): Promise<IParameter[]> {
    if (!(await programService.findById(programId))) {
      throw new AppError(PROGRAM_NOT_FOUND, 404)
    }
    return database
      .select()
      .from(parameters)
      .where(eq(parameters.programId, programId))
      .orderBy(asc(parameters.id))
  },

  // *** Parameters start empty and are filled through updates
  async create(programId: number): Promise<IParameter> {
    if (!(await programService.findById(programId))) {
      throw new AppError(PROGRAM_NOT_FOUND, 404)
    }
    const [parameter] = await database
      .insert(parameters)
      .values({
        name: '',
        description: '',
        example: '',
        inputType: '',
        isRequired: false,
        programId
      })
      .returning()
    return parameter
  },

  async update(id: number, data: IParameterUpdateData): Promise<IParameter> {
    const [parameter] = await database
      .update(parameters)
      .set({
        name: data.name,
        description: data.description,
        example: data.example,
        inputType: data.input_type,
        isRequired: data.isRequired
      })
      .where(eq(parameters.id, id))
      .returning()
    if (!parameter) throw new AppError(PARAMETER_NOT_FOUND, 404)
    return parameter
  },

  async delete(id: number): Promise<IParameter> {
    const [parameter] = await database
      .delete(parameters)
      .where(eq(parameters.id, id))
      .returning()
    if (!parameter) throw new AppError(PARAMETER_NOT_FOUND, 404)
    return parameter
  }
}
