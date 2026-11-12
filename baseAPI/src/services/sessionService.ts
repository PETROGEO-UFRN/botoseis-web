import { AuthError } from '@/errors/AuthError'
import { passwordService } from '@/services/passwordService'
import { tokenService } from '@/services/tokenService'
import { userService } from '@/services/userService'

export const sessionService = {
  // *** Returns the session token for valid credentials
  async create(email: string, password: string): Promise<string> {
    const user = await userService.findByEmail(email)
    if (!user || !(await passwordService.check(password, user.password))) {
      throw new AuthError('Invalid email or password')
    }

    return tokenService.sign({
      id: user.id,
      name: user.name,
      email: user.email
    })
  },

  validate(token: string | undefined) {
    if (!token) throw new AuthError('No token')
    return tokenService.verify(token)
  }
}
