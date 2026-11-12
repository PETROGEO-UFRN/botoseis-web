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

// *** Requires at least one of the given keys to be present
export const atLeastOneOf =
  (keys: readonly string[]) => (data: Record<string, unknown>) => {
    if (Object.keys(data).length === 0) return false
    return keys.some(key => data[key] !== undefined)
  }

export const atLeastOneOfMessage = (keys: readonly string[]) =>
  `At least one of [${keys.map(key => `'${key}'`).join(', ')}] is required.`

// *** Groups issues by top level field, matching the legacy error body
export function toValidationMessages(error: ZodError): IValidationMessages {
  const messages: IValidationMessages = {}
  for (const issue of error.issues) {
    const field = issue.path.length > 0 ? String(issue.path[0]) : '_schema'
    messages[field] = [...(messages[field] ?? []), issue.message]
  }
  return messages
}
