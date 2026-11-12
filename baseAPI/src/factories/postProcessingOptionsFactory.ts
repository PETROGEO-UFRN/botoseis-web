export type IPostProcessingOptionValue = string | number | boolean

export interface IPostProcessingOptions {
  // *** client side program used at the end of the workflow
  key: string
  // *** settings for that program, the format depends on the key
  options: Record<string, IPostProcessingOptionValue>
}

export const DEFAULT_POST_PROCESSING_KEY = 'tab-vizualizer'

// *** Stringified JSON stored at workflows_table.post_processing_options,
// *** set to the visualizer with no options by default
export function createPostProcessingOptions({
  key = DEFAULT_POST_PROCESSING_KEY,
  options = {}
}: Partial<IPostProcessingOptions> = {}): string {
  return JSON.stringify({ key, options })
}

export function parsePostProcessingOptions(
  storedOptions: string | null
): Partial<IPostProcessingOptions> {
  return JSON.parse(storedOptions || '{}')
}
