import jwt from 'jsonwebtoken'

import { authConfig } from '@/config/auth'
import { AuthError } from '@/errors/AuthError'

export const UUID_PATTERN =
  /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i

export interface ITokenPayload {
  id: string
  name: string | null
  email: string | null
}

export const tokenService = {
  // *** No expiration claim, sessions last while the cookie does
  sign(payload: ITokenPayload): string {
    return jwt.sign(payload, authConfig.secret, {
      algorithm: 'HS256',
      noTimestamp: true
    })
  },

  verify(token: string): ITokenPayload {
    let payload: string | jwt.JwtPayload
    try {
      payload = jwt.verify(token.replace('Bearer ', ''), authConfig.secret, {
        algorithms: ['HS256']
      })
    } catch (error) {
      if (error instanceof jwt.TokenExpiredError) {
        throw new AuthError('Expired Token')
      }
      if (
        error instanceof jwt.JsonWebTokenError &&
        error.message === 'invalid signature'
      ) {
        throw new AuthError('Invalid Token Signature')
      }
      throw new AuthError()
    }

    // *** User ids are UUIDs, any other id makes the token invalid
    if (
      typeof payload === 'string' ||
      typeof payload.id !== 'string' ||
      !UUID_PATTERN.test(payload.id)
    ) {
      throw new AuthError()
    }
    return payload as ITokenPayload
  }
}
