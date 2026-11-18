The form's timeout isn't something I can change, so here are the questions as a plain message. There's no time limit; reply whenever you're ready, e.g. "1a 2a 3a 4abd 5a".

1. HTTP contract
   The pytest suite pins the current Flask contract:
   - verb-style URLs (/user/create, /project/list, /line/update/<id>, /command/order/<workflowId>, /programs/groups/create)
   - flat JSON bodies, no response envelope, mixed field casing (program_id, is_active, workflowId, created_at, modified_at)
   - errors as {"Error": "..."}; validation errors as {"Error": {"field": ["msg"]}} with status 422
   - 404 "No instance found for this id" when an entity is missing or not yours
   - program create/update only accept form data (JSON gets 415)
   - UUID user ids, integer ids everywhere else
   Some paths no test covers are broken in Flask today. For example, programs update writes to the request data instead of the database row, and command show crashes on a missing id.
   a) Keep exactly what pytest asserts and fix the untested bugs. pytest stays unchanged as the acceptance suite. (recommended)

2. Database and test reset
   Every test class resets the database with Flask's drop_all/create_all, which only knows the Flask tables. The tests also expect ids to restart at 1 (GET /workflow/show/1 expects 404 on an empty database).
   a) baseAPI owns its schema through Drizzle migrations. conftest resets with plain SQL: TRUNCATE ... RESTART IDENTITY CASCADE on every table except the migrations table. This works against Flask too. (recommended)

3. Data model
   Flask stores some things awkwardly:
   - command order as an integer array in a separate table
   - workflow parents in an association table where only one of projectId/lineId/datasetId is set
   - lines and commands owned by owner_email instead of a user id
   - JSON stored as text
   The HTTP output stays the same whichever you pick.
   b) Port the Flask tables as they are. The workarround are there to fix issues and if eventually fixed, you require extra care an manual human closer review.

4. File domain to leave out (choose all that apply)
   a) su-file, su-file-path, helper-file and dataset routes, and their tests. (recommended)
   c) The uploaded executable 'file' on program create/update. path_to_executable_file stays a plain text field.

5. Auth on admin routes, and extras
   In Flask, /programs, /programs/groups and /programs/parameters have no auth at all, and users.is_admin exists but nothing ever sets it. Requiring admin would break those tests, since the test user isn't an admin.
   d) Like (a), but no Vitest, so pytest is the only test suite.

Already settled, nothing to answer:
- Pushing works through the GitHub App, to chore/remake/server, from a separate clone.
- pytest runs against db-test here.
- One conventional commit per domain.
- No mention of LandWave anywhere, and no PR.