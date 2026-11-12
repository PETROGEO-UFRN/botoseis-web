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
  cli/                    programs catalog scripts
drizzle/                  SQL migrations
data/su_programs/         programs catalog files
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
| `pnpm programs:*`    | programs catalog, see below              |

## Routes

Access: `public`; `session` needs the session cookie; `owner` also requires
the entity at the route to belong to the session user (404 when it does not
exist, 401 when it belongs to someone else).

| Route                                              | Access  |
| -------------------------------------------------- | ------- |
| `POST /user/create`, `GET /user/list`              | public  |
| `PUT /user/update`, `DELETE /user/delete`          | session |
| `POST /session/`, `GET /session/validate`          | public  |
| `GET /project/list`, `POST /project/create`        | session |
| `PUT /project/update/:id`                          | owner   |
| `DELETE /project/delete/:id`                       | owner   |
| `GET /project/root-workflows/list/:id`             | owner   |
| `GET /line/list/:projectId`                        | owner   |
| `POST /line/create/:projectId`                     | owner   |
| `PUT /line/update/:lineId`                         | owner   |
| `DELETE /line/delete/:lineId`                      | owner   |
| `GET /workflow/show/:id`                           | owner   |
| `POST /workflow/create/:parentId`                  | owner   |
| `PUT /workflow/update/:workflowId/name`            | owner   |
| `PUT /workflow/update/:workflowId/file`            | owner   |
| `PUT /workflow/update/:workflowId/output-name`     | owner   |
| `PUT /workflow/update/:workflowId/post-processing` | owner   |
| `DELETE /workflow/delete/:id`                      | owner   |
| `GET /command/show/:id`                            | owner   |
| `POST /command/create/:workflowId`                 | owner   |
| `PUT /command/update/:id/parameters`               | owner   |
| `PUT /command/update/:id/is_active`                | owner   |
| `PUT /command/order/:workflowId`                   | owner   |
| `DELETE /command/delete/:id`                       | owner   |
| `/programs/groups/{list,create,update,delete}`     | public  |
| `/programs/{list,create,update,delete}`            | public  |
| `/programs/parameters/{list,create,update,delete}` | public  |

Program create and update only accept form bodies (urlencoded or multipart).
Errors answer `{ "Error": "message" }`; validation errors answer 422 with
`{ "Error": { "field": ["message"] } }`.

## Tests

The Flask integration suite drives this API over HTTP, with the server on port
8080 and both sides on the same test database. From the repository root,
`make test` starts the `db-test` container (port 5431) and migrates it; the
Flask migrations build the same schema as `drizzle/`, so baseAPI runs on it
as is.

```bash
make test

# baseAPI/
DATABASE_URL=postgresql://admin:mysecretpassword@localhost:5431/admin \
  NODE_ENV=test PORT=8080 pnpm server:dev

# server/, in another terminal, with the Python dev requirements installed
pytest -m "not file_routes"
```

On a database without the Flask migrations, run `pnpm db:migrate` first and
point the tests at it with `TEST_DATABASE_URL`. Never run both migration sets
on one database. Every test class truncates the public tables, so never point
the tests at a database holding real data.

## Programs catalog

The program groups, programs and parameters offered to workflows come from the
Seismic Unix documentation. The catalog lives in `data/su_programs/`, one file
per program group.

| Script                     | Purpose                                                                 |
| -------------------------- | ----------------------------------------------------------------------- |
| `pnpm programs:populate`   | load the catalog files into the database; only runs on an empty catalog |
| `pnpm programs:export [f]` | write the database catalog to `f` (default `data/programs_export.json`) |
| `pnpm programs:write-docs` | rebuild the catalog files from the Seismic Unix sources                 |

`programs:write-docs` reads `SU_SOURCES_DIR` (default
`~/SeismicUnix/src/su/main`) and writes to `PROGRAMS_CATALOG_DIR` (default
`data/su_programs`).
