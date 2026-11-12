import { readdirSync, readFileSync } from 'node:fs'
import path from 'node:path'
import { count } from 'drizzle-orm'

import {
  type IProgramsCatalog,
  PROGRAMS_CATALOG_DIR
} from '@/cli/programsCatalog'
import database from '@/database/connection'
import { parameters, programGroups, programs } from '@/models/index'

// *** Loads the catalog files into an empty program catalog. Running it on a
// *** populated database would duplicate programs, so it refuses to.
async function populatePrograms(): Promise<void> {
  const [{ total }] = await database.select({ total: count() }).from(programs)
  if (total > 0) {
    console.warn('Database alredy initialized. Can only populate empty tables')
    return
  }

  const catalogFiles = readdirSync(PROGRAMS_CATALOG_DIR)
    .filter(fileName => fileName.endsWith('.json'))
    .sort()

  let loadedPrograms = 0
  await database.transaction(async transaction => {
    for (const fileName of catalogFiles) {
      const catalog: IProgramsCatalog = JSON.parse(
        readFileSync(path.join(PROGRAMS_CATALOG_DIR, fileName), 'utf-8')
      )

      for (const groupInfo of catalog.programGroups) {
        const [group] = await transaction
          .insert(programGroups)
          .values({ name: groupInfo.name, description: groupInfo.description })
          .returning({ id: programGroups.id })

        for (const programInfo of groupInfo.programs) {
          const [program] = await transaction
            .insert(programs)
            .values({
              name: programInfo.name,
              description: programInfo.description,
              pathToExecutableFile: programInfo.path_to_executable_file,
              groupId: group.id
            })
            .returning({ id: programs.id })

          if (programInfo.parameters.length > 0) {
            await transaction.insert(parameters).values(
              programInfo.parameters.map(parameterInfo => ({
                name: parameterInfo.name,
                description: parameterInfo.description,
                example: parameterInfo.example,
                inputType: parameterInfo.input_type,
                isRequired: parameterInfo.isRequired,
                programId: program.id
              }))
            )
          }
          loadedPrograms += 1
        }
      }
      console.log(`Loaded ${fileName}`)
    }
  })

  console.log(`Posted ${loadedPrograms} programs into the database`)
}

await populatePrograms()
await database.$client.end()
