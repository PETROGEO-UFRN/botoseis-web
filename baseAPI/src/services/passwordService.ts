import bcrypt from 'bcryptjs'

import { authConfig } from '@/config/auth'

// *** Hashes are stored as the bytes of the bcrypt string, as Flask does
export const passwordService = {
  async hash(password: string): Promise<Buffer> {
    const hash = await bcrypt.hash(password, authConfig.passwordSaltRounds)
    return Buffer.from(hash)
  },

  async check(password: string, hash: Buffer | null): Promise<boolean> {
    if (!hash) return false
    return bcrypt.compare(password, hash.toString())
  }
}
