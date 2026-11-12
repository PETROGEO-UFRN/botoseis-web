import { mkdirSync, readdirSync, statSync, writeFileSync } from 'node:fs'
import path from 'node:path'

import {
  MissingDocError,
  parseProgramDoc,
  readProgramDoc
} from '@/cli/programDocsReader'
import {
  type ICatalogProgramGroup,
  type IProgramsCatalog,
  PROGRAMS_CATALOG_DIR,
  SU_SOURCES_DIR,
  toCatalogJson
} from '@/cli/programsCatalog'

// *** Builds the catalog from the Seismic Unix sources, one file per folder
function writeProgramsDocs(): void {
  mkdirSync(PROGRAMS_CATALOG_DIR, { recursive: true })

  for (const folderName of readdirSync(SU_SOURCES_DIR).sort()) {
    const folderPath = path.join(SU_SOURCES_DIR, folderName)
    if (!statSync(folderPath).isDirectory()) continue

    console.debug(`Current group: ${folderName}`)
    const catalog: IProgramsCatalog = { count_programs: 0, programGroups: [] }
    const programGroup: ICatalogProgramGroup = {
      name: folderName,
      description: '',
      programs: []
    }

    for (const fileName of readdirSync(folderPath).sort()) {
      if (!fileName.endsWith('.c')) continue

      try {
        const sdoc = readProgramDoc(path.join(folderPath, fileName))
        programGroup.programs.push(parseProgramDoc(sdoc))
      } catch (error) {
        if (error instanceof MissingDocError) {
          console.debug(`Value error for program: ${fileName}`)
          continue
        }
        console.error(`Some error occurred with program: ${fileName}`)
        console.error(error)
        process.exit(1)
      }
    }

    if (programGroup.programs.length > 0) {
      catalog.programGroups.push(programGroup)
      catalog.count_programs += programGroup.programs.length
    }

    writeFileSync(
      path.join(PROGRAMS_CATALOG_DIR, `${folderName}.json`),
      toCatalogJson(catalog, 4)
    )
  }
}

writeProgramsDocs()
