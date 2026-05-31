import type { ReactNode } from 'react'

import { GroupContainerStack, GroupContentStack, GroupTitle } from './styles'

interface IGroupProps {
  children?: ReactNode
  title?: string
  direction?: 'row' | 'column'
  largePadding?: boolean
}

export function Group({
  children,
  title,
  direction = 'column',
  largePadding = false
}: IGroupProps & { largePadding?: boolean }) {
  return (
    <GroupContainerStack direction="column">
      {title && <GroupTitle>{title}</GroupTitle>}
      <GroupContentStack largePadding={largePadding} direction={direction}>
        {children}
      </GroupContentStack>
    </GroupContainerStack>
  )
}
