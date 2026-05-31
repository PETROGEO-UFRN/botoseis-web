import IconButton from '@mui/material/IconButton'
import Stack from '@mui/material/Stack'
import { styled } from '@mui/material/styles'
import Typography from '@mui/material/Typography'

interface IRootCustomStack {
  fullSize?: boolean
}

interface IGroupContentStack {
  largePadding?: boolean
}

export const RootCustomStack = styled(Stack)<IRootCustomStack>(
  ({ fullSize, theme }) => ({
    height: fullSize ? '100%' : 'auto',
    margin: theme.spacing(2),
    gap: theme.spacing(3)
  })
)

export const GroupContainerStack = styled(Stack)(({ theme }) => ({
  gap: theme.spacing(1),
  minWidth: theme.spacing(30),
  '&:not(:last-of-type)': {
    paddingBottom: theme.spacing(2),
    borderBottom: `1px solid ${theme.palette.divider}`
  }
}))

export const GroupContentStack = styled(Stack)<IGroupContentStack>(
  ({ largePadding, theme }) => ({
    gap: largePadding ? theme.spacing(2) : theme.spacing(0.5)
  })
)

export const GroupTitle = styled(Typography)(({ theme }) => ({
  color: theme.palette.text.secondary,
  textTransform: 'uppercase',
  letterSpacing: 2
}))

export const CloseIconButton = styled(IconButton)(({ theme }) => ({
  position: 'absolute',
  color: theme.palette.error.main,
  top: theme.spacing(1),
  right: theme.spacing(2)
}))
