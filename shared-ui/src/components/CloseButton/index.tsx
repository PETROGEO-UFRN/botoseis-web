import CloseRoundedIcon from '@mui/icons-material/CloseRounded';

import { IFloatButtonProps } from '../../types/buttonTypes'
import { Container } from './styles'

interface ICloseButtonProps extends IFloatButtonProps {
  size?: 'small' | 'medium' | 'large'
  onClick: () => void
}

export default function CloseButton({
  size = "small",
  onClick,

  $top,
  $bottom,
  $left,
  $right,
}: ICloseButtonProps) {
  return (
    <Container
      color='error'
      size='small'
      onClick={onClick}

      $top={$top}
      $bottom={$bottom}
      $left={$left}
      $right={$right}
    >
      <CloseRoundedIcon fontSize={size} />
    </Container>
  )
}
