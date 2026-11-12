import path from 'node:path'

// *** Catalog files, one per program group folder: the format read by
// *** "programs:populate" and written by "programs:write-docs"
export interface ICatalogParameter {
  name: string
  description: string
  example: string
  input_type: 'integer' | 'float' | 'string' | string
  isRequired: boolean
}

export interface ICatalogProgram {
  name: string
  description: string
  path_to_executable_file: string
  parameters: ICatalogParameter[]
}

export interface ICatalogProgramGroup {
  name: string
  description: string
  programs: ICatalogProgram[]
}

export interface IProgramsCatalog {
  count_programs: number
  programGroups: ICatalogProgramGroup[]
}

export const PROGRAMS_CATALOG_DIR = path.resolve(
  process.env.PROGRAMS_CATALOG_DIR || 'data/su_programs'
)

// *** Seismic Unix main sources, one folder per program group
export const SU_SOURCES_DIR = path.resolve(
  process.env.SU_SOURCES_DIR ||
    path.join(process.env.HOME || '', 'SeismicUnix/src/su/main')
)

// *** Same layout as Python json.dump with ensure_ascii, so regenerated files
// *** keep their diff small
export function toCatalogJson(data: unknown, indent: number): string {
  return JSON.stringify(data, null, indent).replace(
    /[\u0080-\uffff]/g,
    character => `\\u${character.charCodeAt(0).toString(16).padStart(4, '0')}`
  )
}
