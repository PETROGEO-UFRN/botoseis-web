import { type ZodError, z } from 'zod'

import type { IValidationMessages } from '@/errors/ValidationError'

export const MESSAGES = {
  required: 'Missing data for required field.',
  invalidInput: 'Invalid input type.',
  string: 'Not a valid string.',
  integer: 'Not a valid integer.',
  boolean: 'Not a valid boolean.',
  list: 'Not a valid list.',
  mapping: 'Not a valid mapping type.',
  email: 'Not a valid email address.'
} as const

export const IdSchema = z.coerce.number().int().positive()

const requiredOr = (typeMessage: string) => ({
  error: (issue: { input: unknown }) =>
    issue.input === undefined ? MESSAGES.required : typeMessage
})

export const requiredString = () => z.string(requiredOr(MESSAGES.string))

export const requiredInteger = () =>
  z.number(requiredOr(MESSAGES.integer)).int({ error: MESSAGES.integer })

export const requiredBoolean = () => z.boolean(requiredOr(MESSAGES.boolean))

export const requiredEmail = () =>
  z.email({
    error: issue =>
      issue.input === undefined
        ? MESSAGES.required
        : typeof issue.input === 'string'
          ? MESSAGES.email
          : MESSAGES.string
  })

export const requiredEnum = <const T extends readonly [string, ...string[]]>(
  values: T
) =>
  z.enum(values, {
    error: issue =>
      issue.input === undefined
        ? MESSAGES.required
        : `Must be one of: ${values.join(', ')}.`
  })

export const optionalString = () => z.string({ error: MESSAGES.string })

export const optionalBoolean = () => z.boolean({ error: MESSAGES.boolean })

// *** Bodies must be objects, anything else fails as a whole
export const requestBody = <T extends z.ZodRawShape>(shape: T) =>
  z.object(shape, { error: MESSAGES.invalidInput })

// *** Update bodies need one known field at least, unknown ones are dropped
export const hasAnyField = (data: Record<string, unknown>) =>
  Object.values(data).some(value => value !== undefined)

export const AT_LEAST_ONE_FIELD = 'At least one field must be provided.'

// *** Groups issues by top level field, matching the legacy error body
export function toValidationMessages(error: ZodError): IValidationMessages {
  const messages: IValidationMessages = {}
  for (const issue of error.issues) {
    const field = issue.path.length > 0 ? String(issue.path[0]) : '_schema'
    messages[field] = [...(messages[field] ?? []), issue.message]
  }
  return messages
}
