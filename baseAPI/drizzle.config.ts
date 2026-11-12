import { defineConfig } from 'drizzle-kit'
import { databaseConfig } from './src/config/database'

export default defineConfig({
  schema: './src/models/index.ts',
  dialect: 'postgresql',
  dbCredentials: {
    url: databaseConfig.url
  },
  out: './drizzle',
  verbose: true,
  strict: true
})
