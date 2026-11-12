import { drizzle } from 'drizzle-orm/node-postgres'
import { Pool } from 'pg'
import { databaseConfig } from '@/config/database'
import * as schema from '@/models/index'

const pool = new Pool({
  connectionString: databaseConfig.url
})

export const database = drizzle(pool, { schema })

export type IDatabase = typeof database
export type ITransaction = Parameters<
  Parameters<IDatabase['transaction']>[0]
>[0]

export default database
