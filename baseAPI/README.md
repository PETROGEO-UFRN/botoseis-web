# Base API

Node.js reimplementation of the Botoseis server API for the base entities:
users, sessions, projects, lines, workflows, commands and the program catalog
(program groups, programs and parameters). File routes (su-file, su-file-path,
helper-file and dataset) are not part of this app.

The HTTP contract matches the Flask server (`server/`): same URLs, request
bodies, response bodies, status codes and the `Authorization` session cookie.
The Flask integration suite at `server/app/tests` is the acceptance test.

## Stack

- [Koa](https://koajs.com/) with `@koa/router`, `@koa/cors` and `koa-body`
- [Drizzle ORM](https://orm.drizzle.team/) on PostgreSQL (`pg`)
- [Zod](https://zod.dev/) for request validation
- `jsonwebtoken` (HS256) and `bcryptjs` for sessions and passwords
- [Biome](https://biomejs.dev/) for linting and formatting

## Layout

```
src/
  app.ts                  app factory: middlewares and routers
  server.ts               HTTP entry point
  config/                 environment, database and CORS settings
  database/connection.ts  Drizzle client
  errors/                 AppError, AuthError and ValidationError
  models/                 Drizzle tables, one file per table
  presentation/
    middlewares/          error handler, validation, authentication
    routes/               one router factory per domain
    schemas/              Zod request schemas
    serializers/          response bodies
  services/               domain logic and database access
drizzle/                  SQL migrations
```

## Setup

```bash
pnpm install
cp .env.example .env    # then fill SECRET and DATABASE_URL
pnpm db:migrate
pnpm server:dev
```

| Variable       | Default                                                    |
| -------------- | ---------------------------------------------------------- |
| `NODE_ENV`     | `development` (`production` and `test` also accepted)      |
| `PORT`         | `5000`                                                     |
| `SECRET`       | `private_key`, the JWT signing secret                      |
| `DATABASE_URL` | `postgresql://admin:mysecretpassword@localhost:5432/admin` |

Outside `development`, authentication errors answer `Not authorized` without
details. In `production` the session cookie uses `SameSite=None` and CORS only
accepts the configured client origins.

## Scripts

| Script               | Purpose                                  |
| -------------------- | ---------------------------------------- |
| `pnpm server:dev`    | run with reload                          |
| `pnpm server:prod`   | run once                                 |
| `pnpm typecheck`     | TypeScript check                         |
| `pnpm lint`          | Biome check, applying safe fixes         |
| `pnpm db:generate`   | generate a migration from `src/models`   |
| `pnpm db:migrate`    | apply the migrations in `drizzle/`       |
