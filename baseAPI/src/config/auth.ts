export const authConfig = {
  // *** JWT signing secret (HS256)
  secret: process.env.SECRET || 'private_key',
  cookieName: 'Authorization',
  // *** same cost as the default bcrypt salt of the Flask server
  passwordSaltRounds: 12
}
