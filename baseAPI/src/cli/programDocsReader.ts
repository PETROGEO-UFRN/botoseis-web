import { readFileSync } from 'node:fs'

import type { ICatalogParameter, ICatalogProgram } from '@/cli/programsCatalog'

export class MissingDocError extends Error {}

const UTF8 = new TextDecoder('utf-8', { fatal: true })

const SDOC_PATTERN = /char\s*\*?\s*sdoc\s*\[\]?\s*=\s*\{([\s\S]*?)\};/
const PARAMETER_PATTERN = /^(\w+)=([\w,.()]+)\s+(.*)/

// *** Lines of the self documentation ("sdoc") array of a Seismic Unix
// *** program source, without quotes and trailing commas
export function readProgramDoc(programPath: string): string[] {
  let content: string
  try {
    content = UTF8.decode(readFileSync(programPath))
  } catch {
    // *** sources that are not valid UTF-8 are skipped, as on the Python CLI
    throw new MissingDocError(`Not a UTF-8 file: ${programPath}`)
  }
  const match = SDOC_PATTERN.exec(content)
  if (!match) throw new MissingDocError(`No match for program: ${programPath}`)

  return match[1]
    .split(/\r\n|\r|\n/)
    .filter(line => new Set(line).size > 3)
    .map(line => line.replaceAll('"', '').slice(0, -1).trim())
    .filter(line => line.length > 0)
}

export function detectType(value: string): 'integer' | 'float' | 'string' {
  if (/^\d+$/.test(value)) return 'integer'
  if (/^\d+\.\d+$/.test(value)) return 'float'
  return 'string'
}

function readDescription(sdocLines: string[]): string {
  const [firstLine] = sdocLines
  if (firstLine.includes('-')) {
    return firstLine.slice(firstLine.indexOf('-') + 1).trim()
  }
  if (sdocLines.length > 1 && sdocLines[1].trim() === '') {
    return sdocLines.length > 2 ? sdocLines[2].trim() : ''
  }
  return sdocLines.length > 1 ? sdocLines[1].trim() : ''
}

// *** The first line names the program; "name=example description" lines are
// *** parameters, required after a "Required" line and optional after an
// *** "Optional" one
export function parseProgramDoc(sdocLines: string[]): ICatalogProgram {
  const name = sdocLines[0]?.split(/\s+/).filter(Boolean)[0]
  if (!name) {
    throw new Error(
      `Error in extracting the sdoc for sdoc: ${JSON.stringify(sdocLines)}`
    )
  }

  const parameters: ICatalogParameter[] = []
  let isRequired = false
  for (const line of sdocLines) {
    if (line.includes('Required')) isRequired = true
    else if (line.includes('Optional')) isRequired = false

    const match = PARAMETER_PATTERN.exec(line)
    if (match) {
      parameters.push({
        name: match[1],
        description: match[3].trim(),
        example: match[2],
        input_type: detectType(match[2]),
        isRequired
      })
    }
  }

  return {
    name,
    description: readDescription(sdocLines),
    path_to_executable_file: name,
    parameters
  }
}
