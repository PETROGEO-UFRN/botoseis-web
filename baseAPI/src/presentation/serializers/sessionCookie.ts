import { authConfig } from '@/config/auth'

// *** Built by hand: Koa refuses Secure cookies on plain HTTP connections,
// *** while browsers still accept them from localhost
export function serializeSessionCookie(
  token: string,
  environment: environmentType
): string {
  const sameSite = environment === 'production' ? 'None' : 'Lax'
  return [
    `${authConfig.cookieName}=${token}`,
    'Secure',
    'HttpOnly',
    'Path=/',
    `SameSite=${sameSite}`
  ].join('; ')
}
