const ENVIRONMENTS: environmentType[] = ['development', 'production', 'test']

export function getEnvironment(): environmentType {
  const environment = process.env.NODE_ENV as environmentType | undefined
  return environment && ENVIRONMENTS.includes(environment)
    ? environment
    : 'development'
}
