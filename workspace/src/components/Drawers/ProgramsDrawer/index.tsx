import { useState, useEffect } from 'react'
import type { Dispatch, SetStateAction } from 'react'

import { useShallow } from 'zustand/react/shallow'

import { CloseButton } from 'shared-ui';

import { clientProgramsGroup } from 'constants/clientPrograms'
import { postProcessingCommands, StaticTabKey } from 'constants/staticCommands';
import { getGroups } from 'services/programServices'
import { createNewCommand } from 'services/commandServices'
import { updateWorkflowPostProcessing } from 'services/workflowServices'
import { useSelectedWorkflowsStore } from 'store/selectedWorkflowsStore';
import { useCommandsStore } from 'store/commandsStore';
import useNotificationStore from 'store/notificationStore';

import GenericDrawer from "../GenericDrawer"
import ProgramsGroupsAccordion from './ProgramsGroupsAccordion';
import {
  Container,
} from './styles'

type expandedGroupKey = 'Client' | 'SeismicUnix' | undefined

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

  const [expandedGroup, setExpandedGroup] = useState<expandedGroupKey>('SeismicUnix')

  // *** Groups of Commands, available commands to insert in the workflow
  const [programsGroups, setProgramsGroups] = useState<Array<IProgramsGroup>>([])

  const handleExpandedGroupChange = (key: expandedGroupKey) => {
    if (expandedGroup == key)
      setExpandedGroup(undefined)
    setExpandedGroup(key)
  }

  const addProgramToCurrentWorkflow = (name: string, program_id: number) => {
    if (singleSelectedWorkflowId)
      return createNewCommand(
        singleSelectedWorkflowId,
        program_id,
        name
      ).then((result) => {
        if (!result) return;
        const newCommands = [...commands]
        const postProcessingStaticTabsAmount = 2
        newCommands.splice(newCommands.length - postProcessingStaticTabsAmount, 0, result)
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
    _name: string,
    program_id: clientProgramIdType
  ) => {
    if (singleSelectedWorkflowId)
      // *** Shall overwrite the past post processing key
      // *** That allows only one post processing program at time
      return updateWorkflowPostProcessing({
        workflowId: singleSelectedWorkflowId,
        key: program_id,
      }).then((workflow) => {
        const tempCommands = [...commands]

        const lastCommandId = tempCommands[tempCommands.length - 1].id
        if (
          lastCommandId == StaticTabKey.Velan ||
          lastCommandId == StaticTabKey.Vizualizer
        )
          tempCommands.pop()

        const newCommand = postProcessingCommands.find((command) =>
          command.id == workflow?.post_processing_options?.key
        )
        if (!newCommand)
          return

        setCommands([
          ...tempCommands,
          newCommand,
        ])
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

        {/* Type parameter to accept client-side-only programs */}
        <ProgramsGroupsAccordion<clientProgramIdType>
          packageTitle="Boto - Interative"
          programsGroups={[clientProgramsGroup]}
          addProgramToCurrentWorkflow={addClientProgramToCurrentWorkflow}
          isExpanded={expandedGroup == 'Client'}
          onChange={() => handleExpandedGroupChange('Client')}
        />

        <ProgramsGroupsAccordion
          packageTitle="Seismic Unix"
          programsGroups={programsGroups}
          addProgramToCurrentWorkflow={addProgramToCurrentWorkflow}
          isExpanded={expandedGroup == 'SeismicUnix'}
          onChange={() => handleExpandedGroupChange('SeismicUnix')}
        />
      </Container>
    </GenericDrawer>
  )
}
