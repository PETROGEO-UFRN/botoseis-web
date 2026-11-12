import { customType } from 'drizzle-orm/pg-core'

// *** Raw bytes, used for the bcrypt password hash
export const bytea = customType<{ data: Buffer; driverData: Buffer }>({
  dataType() {
    return 'bytea'
  }
})
