import Stack from '@mui/material/Stack'
import { styled } from '@mui/material/styles'
import TextField from '@mui/material/TextField'

interface IRootContainerProps {
  fullwidth?: boolean
}

export const RootContainer = styled(Stack)<IRootContainerProps>(
  ({ theme, fullwidth }) => ({
    zIndex: 10,
    position: 'absolute',
    top: 0,
    left: 0,
    width: fullwidth ? '100%' : 'auto',

    gap: theme.spacing(2),
    padding: theme.spacing(2),
    paddingTop: theme.spacing(1),
    paddingBottom: theme.spacing(1),
    borderEndEndRadius: fullwidth ? 0 : theme.shape.borderRadius,
    backgroundColor: theme.palette.grey[200],
    boxShadow: theme.shadows[3]
  })
)

export const NavigationTextField = styled(TextField)({
  minWidth: 128,
  paddingBottom: 0,
  input: {
    padding: 0,
    MozAppearance: 'textfield'
  },
  '& input::-webkit-outer-spin-button, & input::-webkit-inner-spin-button': {
    WebkitAppearance: 'none',
    margin: 0
  }
})
