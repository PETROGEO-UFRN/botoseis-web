import { useState } from "react"

import DeleteForeverRoundedIcon from '@mui/icons-material/DeleteForeverRounded';

import {
  CustomIconButton,
  CustomButton,
} from "./styles"

interface IDeleteButtonProps {
  onRemove(): void
  size?: "small" | "medium" | "large"
}

export default function DeleteButton({
  onRemove,
  size = "large"
}: IDeleteButtonProps) {
  const [allowDelete, setAllowDelete] = useState(false)

  const displayDeleteButton = (event: React.MouseEvent<HTMLButtonElement>) => {
    event.stopPropagation()
    setAllowDelete(true)
    setTimeout(() => {
      setAllowDelete(false)
    }, 4000);
  }

  const deleteEntity = (event: React.MouseEvent<HTMLButtonElement>) => {
    event.stopPropagation()
    onRemove()
  }

  return (
    <CustomIconButton
      onClick={displayDeleteButton}
      color="error"
      size={size}
      disableRipple={allowDelete}
      $isHoverDisable={allowDelete}
    >
      <CustomButton
        onClick={deleteEntity}
        variant="contained"
        size={size}
        color="error"
        $isHidden={!allowDelete}
      >
        Deletar
      </CustomButton>
      <DeleteForeverRoundedIcon color="error" fontSize={size} />
    </CustomIconButton>
  )
}
