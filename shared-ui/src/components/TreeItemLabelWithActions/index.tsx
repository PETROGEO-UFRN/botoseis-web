import { useEffect, useState } from "react";
import { useDebounce } from "use-debounce"
import CircularProgress from '@mui/material/CircularProgress';
import IconButton from "@mui/material/IconButton";
import DriveFileRenameOutlineRoundedIcon from '@mui/icons-material/DriveFileRenameOutlineRounded';

import DeleteButton from "../DeleteButton";
import {
  Container,
  ActionsBox,
  CustomTextField,
} from "./styles"

interface ILabelContentProps {
  labelText: string
  onRemove(): void
  onUpdate?(newName: string): void
}

export default function TreeItemLabelWithActions({
  labelText,
  onRemove,
  onUpdate
}: ILabelContentProps) {
  const [isLoadingUpdate, setIsLoadingUpdate] = useState(false)
  const [labelTextEditing, setLabelTextEditing] = useState(labelText)
  const [labelTextDebounced] = useDebounce(labelTextEditing, 1500)

  useEffect(() => {
    setIsLoadingUpdate(true)
  }, [labelTextEditing])

  useEffect(() => {
    if (onUpdate && labelTextDebounced !== labelText)
      onUpdate(labelTextDebounced)
    setIsLoadingUpdate(false)
  }, [labelTextDebounced])

  return (
    <Container>
      {isLoadingUpdate && <CircularProgress size={16} />}
      <CustomTextField
        id={`label-${labelText}`}
        type="text"
        size="small"
        value={labelTextEditing}
        $isLoadingUpdate={isLoadingUpdate}

        onChange={(event) => setLabelTextEditing(event.target.value)}
        onKeyDown={(event) => event.stopPropagation()}
        onClick={(event) => {
          event.preventDefault()
          event.stopPropagation()
        }}
      />

      <ActionsBox>
        {onUpdate && (
          <IconButton
            size="small"
            onClick={(event) => event.stopPropagation()}
            component="label"
            htmlFor={`label-${labelText}`}
            sx={{ zIndex: 1000 }}
          >
            <DriveFileRenameOutlineRoundedIcon
              color="primary"
              fontSize="small"
            />
          </IconButton>
        )}

        <DeleteButton
          size="small"
          onRemove={onRemove}
        />
      </ActionsBox>
    </Container>
  )
}
