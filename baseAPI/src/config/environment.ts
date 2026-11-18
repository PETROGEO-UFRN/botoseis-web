import { z } from 'zod'

// *** Unknown or missing NODE_ENV values fall back to development
const EnvironmentSchema = z
  .enum(['development', 'production', 'test'])
  .catch('development')

export function getEnvironment(): environmentType {
  return EnvironmentSchema.parse(process.env.NODE_ENV)
}
