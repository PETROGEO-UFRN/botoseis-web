import { useState, useEffect } from 'react'
import type { Dispatch, SetStateAction } from 'react'

import { useShallow } from 'zustand/react/shallow'
import Typography from '@mui/material/Typography';
import List from '@mui/material/List';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Button from '@mui/material/Button';
import Tooltip from '@mui/material/Tooltip';

import KeyboardBackspaceRoundedIcon from '@mui/icons-material/KeyboardBackspaceRounded';
import ExpandMoreRoundedIcon from '@mui/icons-material/ExpandMoreRounded';
import QuestionMarkIcon from '@mui/icons-material/QuestionMark';

import { CloseButton } from 'shared-ui';

import { getGroups } from 'services/programServices'
import { createNewCommand } from 'services/commandServices'
import { useSelectedWorkflowsStore } from 'store/selectedWorkflowsStore';
import { useCommandsStore } from 'store/commandsStore';
import useNotificationStore from 'store/notificationStore';
import GenericDrawer from "../GenericDrawer"


import {
  Container,
  GroupsListBox,
  Title,
  CustomAccordion,
  CustomListItem
} from './styles'

interface IProgramsDrawerProps {
  isOpen: boolean
  setIsOpen: Dispatch<SetStateAction<boolean>>
}

export default function ProgramsDrawer({
  isOpen,
  setIsOpen
}: IProgramsDrawerProps) {
  const triggerNotification = useNotificationStore(useShallow((state) => state.triggerNotification))
  const singleSelectedWorkflowId = useSelectedWorkflowsStore(useShallow((state) => state.singleSelectedWorkflowId))
  // *** Commands in the current selected workflow
  const {
    commands,
    setCommands,
    setSelectedCommandId
  } = useCommandsStore(useShallow((state) => ({
    commands: state.commands,
    setCommands: state.setCommands,
    setSelectedCommandId: state.setSelectedCommandId,
  })))

  // *** Groups of Commands, available commands to insert in the workflow
  const [programsGroups, setProgramsGroups] = useState<Array<IProgramsGroup>>([])

  const addProgramToCurrentWorkflow = (name: string, program_id: number) => {
    if (singleSelectedWorkflowId)
      return createNewCommand(
        singleSelectedWorkflowId,
        program_id,
        name
      ).then((result) => {
        if (!result) return;
        const newCommands = [...commands]
        const posProcessingStaticTabsAmount = 2
        newCommands.splice(newCommands.length - posProcessingStaticTabsAmount, 0, result)
        setCommands(newCommands)

        // *** Turn focous on the new command
        if (typeof result.id !== "number") return
        setSelectedCommandId(result.id)
      })

    triggerNotification({
      content: "Must select an workflow",
      variant: "warning",
    })
  }

  useEffect(() => {
    getGroups().then((result) => {
      setProgramsGroups(result)
    })
  }, [])

  return (
    <GenericDrawer
      isOpen={isOpen}
      setIsOpen={setIsOpen}
      anchor='right'
    >
      <Container>
        <CloseButton
          onClick={() => setIsOpen(false)}
          $top={"8px"}
        />

        <Title variant='h5'>
          Seismic Unix
        </Title>

        <GroupsListBox>
          {programsGroups.map((group) => (
            <CustomAccordion
              key={group.id}
              disableGutters
            >
              <AccordionSummary expandIcon={<ExpandMoreRoundedIcon />}>
                <Typography
                  variant='subtitle1'
                  fontWeight="700"
                >
                  {group.name.toUpperCase()}
                </Typography>
              </AccordionSummary>

              <AccordionDetails>
                <List
                  dense
                  disablePadding
                >
                  {group.programs.map((program) => (
                    <CustomListItem
                      key={program.id}
                      disableGutters
                    >
                      <Button
                        onClick={() => addProgramToCurrentWorkflow(
                          program.path_to_executable_file,
                          program.id,
                        )}
                        variant='text'
                        startIcon={<KeyboardBackspaceRoundedIcon />}
                      >
                        <Typography
                          variant='body1'
                          key={program.id}
                        >
                          {program.name}
                        </Typography>
                      </Button>

                      <Tooltip
                        title={program.description}
                        placement='top'
                        arrow
                      >
                        <QuestionMarkIcon
                          color='primary'
                          fontSize='small'
                        />
                      </Tooltip>
                    </CustomListItem>
                  ))}
                </List>
              </AccordionDetails>
            </CustomAccordion>
          ))}
        </GroupsListBox>

      </Container>
    </GenericDrawer>
  )
}
