import { createContext, useContext, useState } from 'react'
import type { Dispatch, ReactNode, SetStateAction } from 'react'

interface ISelectedProgramProviderProps {
  children: ReactNode | Array<ReactNode>
}

interface SelectedProgramContext {
  selectedProgram: IGenericProgram | null
  setSelectedProgram: Dispatch<SetStateAction<IGenericProgram | null>>
}

const SelectedProgramContext = createContext<SelectedProgramContext>({
  selectedProgram: null,
  setSelectedProgram: () => undefined,
});

export default function SelectedProgramProvider({ children }: ISelectedProgramProviderProps) {
  const [selectedProgram, setSelectedProgram] = useState<IGenericProgram | null>(null)

  return (
    <SelectedProgramContext.Provider
      value={{
        selectedProgram,
        setSelectedProgram
      }}
    >
      {children}
    </SelectedProgramContext.Provider>
  )
}

// eslint-disable-next-line react-refresh/only-export-components
export function useSelectedProgramCommand(): SelectedProgramContext {
  const context = useContext(SelectedProgramContext)
  if (!context)
    throw new Error('useSelectedProgramCommand must be used within a SelectedProgramProvider')
  const {
    selectedProgram,
    setSelectedProgram,
  } = context
  return {
    selectedProgram,
    setSelectedProgram,
  }
}
