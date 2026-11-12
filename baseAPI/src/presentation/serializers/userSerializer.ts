import type { IUser } from '@/models/index'

export function serializeUser(user: IUser) {
  return {
    id: user.id,
    name: user.name,
    email: user.email
  }
}
