import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { useShallow } from 'zustand/react/shallow';

import Tooltip from '@mui/material/Tooltip';
import CloseRoundedIcon from '@mui/icons-material/CloseRounded'
import CommentsDisabledRoundedIcon from '@mui/icons-material/CommentsDisabledRounded';

import { updateCommandIsActive } from 'services/commandServices';
import { useSelectedWorkflowsStore } from 'store/selectedWorkflowsStore';
import { useCommandsStore } from 'store/commandsStore';

import {
  Container,
  TabBody,
  ActionButtonsContainer,
  ActionButton
} from './styles'

// use is_active to turn down opacity
// todo: turn into generic and make two tab components
export default function CustomTab({
  // *** value is usually the related item ID
  value,
  label,
  onRemove,
  $color = "primary",
  $orientation = "horizontal",
  $isActive = true,
  // *** for some reason, "...props" is necessery for tabs component ***
  ...props
}: ICustomTabProps) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
  } = useSortable({ id: value });

  const hasSelectedDataset = useSelectedWorkflowsStore(useShallow((state) => (
    state.hasSelectedDataset
  )))

  const {
    commands,
    setCommands,
  } = useCommandsStore(useShallow((state) => ({
    commands: state.commands,
    setCommands: state.setCommands,
  })))

  // ! This function should not be in a generic component
  const handleUpdateCommandIsActive = () => {
    updateCommandIsActive(value)
    const newCommandsList = commands.map(command => {
      if (
        command.id === value &&
        "is_active" in command
      )
        return {
          ...command,
          is_active: !command.is_active
        }
      return command
    })
    setCommands(newCommandsList)
  }

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  return (
    <>
      <Tooltip title={label} >
        <Container>
          <TabBody
            {...props}
            value={value}
            label={label}
            $color={$color}
            $orientation={$orientation}
            $isActive={$isActive}

            ref={setNodeRef}
            style={style}
            {...attributes}
            {...listeners}
          />
          {
            $orientation == "vertical" &&
            Number.isInteger(value) &&
            !hasSelectedDataset && (
              <ActionButtonsContainer>
                {/* ! comment disabled should not be in generic component */}
                <ActionButton onClick={handleUpdateCommandIsActive}>
                  <CommentsDisabledRoundedIcon />
                </ActionButton>
                <ActionButton onClick={onRemove}>
                  <CloseRoundedIcon />
                </ActionButton>
              </ActionButtonsContainer>
            )
          }
        </Container>
      </Tooltip >
    </>
  )
}
