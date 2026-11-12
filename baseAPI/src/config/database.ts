export const databaseConfig = {
  url:
    process.env.DATABASE_URL ||
    'postgresql://admin:mysecretpassword@localhost:5432/admin'
}
