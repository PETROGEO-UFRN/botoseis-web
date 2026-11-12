// *** Field name to messages, "_schema" holds errors not bound to a field
export type IValidationMessages = Record<string, string[]>

export class ValidationError extends Error {
  readonly statusCode = 422
  readonly messages: IValidationMessages

  constructor(messages: IValidationMessages) {
    super('Validation failed')
    this.name = 'ValidationError'
    this.messages = messages
  }
}
