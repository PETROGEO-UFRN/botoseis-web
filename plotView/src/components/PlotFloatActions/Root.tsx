import type { ReactNode } from 'react'

import { RootContainer } from './styles'

interface IRootProps {
  children?: ReactNode
  fullwidht?: boolean
}

export default function Root({ children, fullwidht }: IRootProps) {
  return (
    <RootContainer direction="row" fullwidth={fullwidht}>
      {children}
    </RootContainer>
  )
}
