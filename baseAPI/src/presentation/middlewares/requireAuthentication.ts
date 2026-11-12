import type Koa from 'koa'

import { authConfig } from '@/config/auth'
import { AppError } from '@/errors/AppError'
import { AuthError } from '@/errors/AuthError'
import type { IUser } from '@/models/index'
import { IdSchema } from '@/presentation/schemas/commonSchemas'
import { tokenService } from '@/services/tokenService'
import { userService } from '@/services/userService'

// *** Ownership of an entity: projects store the user id, other entities
// *** store the owner email
export interface IEntityOwner {
  userId?: string | null
  ownerEmail?: string | null
}

export type IOwnerLoader = (
  context: Koa.Context
) => Promise<IEntityOwner | undefined>

// *** Loads the owner of the entity whose integer id is at the route param
export const ownerByRouteParam =
  (
    findOwner: (id: number) => Promise<IEntityOwner | undefined>,
    paramName: string
  ): IOwnerLoader =>
  async context => {
    const parsed = IdSchema.safeParse(context.params[paramName])
    if (!parsed.success) return undefined
    return findOwner(parsed.data)
  }

function isOwner(owner: IEntityOwner, user: IUser): boolean {
  const ownerKey =
    owner.ownerEmail !== undefined ? owner.ownerEmail : owner.userId
  return ownerKey === user.email || ownerKey === user.id
}

// *** Requires a valid session cookie; when an owner loader is given, the
// *** entity must exist (404) and belong to the session user (401)
export const requireAuthentication = (loadOwner?: IOwnerLoader) => {
  return async (context: Koa.Context, next: Koa.Next) => {
    const token = context.cookies.get(authConfig.cookieName)
    if (!token) throw new AuthError('No token')

    const payload = tokenService.verify(token)
    const user = await userService.findById(payload.id)
    if (!user) throw new AppError('User does not exist', 404)

    if (loadOwner) {
      const owner = await loadOwner(context)
      if (!owner) throw new AppError('No instance found for this id', 404)
      if (!isOwner(owner, user)) {
        throw new AuthError('User unauthorized for this entity')
      }
    }

    context.state.user = user
    await next()
  }
}

export function getAuthenticatedUser(context: Koa.Context): IUser {
  const user = context.state.user
  if (!user) throw new AuthError()
  return user
}
