import { useState, useEffect } from 'react'
import type { Dispatch, SetStateAction } from 'react'

import { useShallow } from 'zustand/react/shallow'

import { CloseButton } from 'shared-ui';

import { clientProgramsGroup } from 'constants/clientPrograms'
import { getGroups } from 'services/programServices'
import { createNewCommand } from 'services/commandServices'
import { useSelectedWorkflowsStore } from 'store/selectedWorkflowsStore';
import { useCommandsStore } from 'store/commandsStore';
import useNotificationStore from 'store/notificationStore';

import GenericDrawer from "../GenericDrawer"
import ProgramsGroupsAccordion from './ProgramsGroupsAccordion';
import {
  Container,
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

  const addClientProgramToCurrentWorkflow = (
    name: string,
    program_id: clientProgramIdType
  ) => {
    console.log(name, program_id);
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

        {/* Type parameter to accept client-side-only programs */}
        <ProgramsGroupsAccordion<clientProgramIdType>
          packageTitle="Boto - Interative"
          programsGroups={[clientProgramsGroup]}
          addProgramToCurrentWorkflow={addClientProgramToCurrentWorkflow}
        />

        <ProgramsGroupsAccordion
          packageTitle="Seismic Unix"
          programsGroups={programsGroups}
          addProgramToCurrentWorkflow={addProgramToCurrentWorkflow}
        />
      </Container>
    </GenericDrawer>
  )
}
