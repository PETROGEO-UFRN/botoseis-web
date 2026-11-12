// *** Status 401; outside development the response hides the message
export class AuthError extends Error {
  readonly statusCode = 401

  constructor(message = 'Request not authorized') {
    super(message)
    this.name = 'AuthError'
  }
}
