const PRODUCTION_ORIGINS = [
  'https://client1.domain.com',
  'https://client2.domain.com'
]

// *** Development and test accept any origin, with credentials
export function isOriginAllowed(
  origin: string,
  environment: environmentType
): boolean {
  if (environment !== 'production') return true
  return PRODUCTION_ORIGINS.includes(origin)
}
