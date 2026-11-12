import type { IUser } from '@/models/index'

declare module 'koa' {
  interface DefaultState {
    // *** set by requireAuthentication
    user?: IUser
  }
}
