import { writeFileSync } from 'node:fs'
import path from 'node:path'
import { asc, eq } from 'drizzle-orm'

import {
  type ICatalogProgramGroup,
  type IProgramsCatalog,
  toCatalogJson
} from '@/cli/programsCatalog'
import database from '@/database/connection'
import { parameters, programGroups, programs } from '@/models/index'

const DEFAULT_OUTPUT_FILE = 'data/programs_export.json'

// *** Writes the database program catalog in the catalog file format
async function exportPrograms(outputFile: string): Promise<void> {
  console.log('Fetching database...')
  const groups = await database
    .select()
    .from(programGroups)
    .orderBy(asc(programGroups.id))

  const programGroupsResult: ICatalogProgramGroup[] = []
  let countPrograms = 0
  for (const group of groups) {
    const groupPrograms = await database
      .select()
      .from(programs)
      .where(eq(programs.groupId, group.id))
      .orderBy(asc(programs.id))

    const catalogPrograms = []
    for (const program of groupPrograms) {
      const programParameters = await database
        .select()
        .from(parameters)
        .where(eq(parameters.programId, program.id))
        .orderBy(asc(parameters.id))

      catalogPrograms.push({
        name: program.name ?? '',
        description: program.description ?? '',
        path_to_executable_file: program.pathToExecutableFile ?? '',
        parameters: programParameters.map(parameter => ({
          name: parameter.name ?? '',
          description: parameter.description ?? '',
          example: parameter.example ?? '',
          input_type: parameter.inputType ?? '',
          isRequired: parameter.isRequired ?? false
        }))
      })
      countPrograms += 1
    }

    programGroupsResult.push({
      name: group.name ?? '',
      description: group.description ?? '',
      programs: catalogPrograms
    })
  }

  const catalog: IProgramsCatalog = {
    count_programs: countPrograms,
    programGroups: programGroupsResult
  }
  writeFileSync(outputFile, toCatalogJson(catalog, 2))

  console.log('Programs exported from database to JSON.')
  console.log('Including entities from this tables:')
  console.log(' - program_groups_table')
  console.log(' - programs_table')
  console.log(' - parameters_table')
  console.log(
    `\nExported ${countPrograms} programs divided in ${groups.length} groups to ${outputFile}`
  )
}

await exportPrograms(path.resolve(process.argv[2] || DEFAULT_OUTPUT_FILE))
await database.$client.end()
