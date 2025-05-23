import { useEffect, useState } from 'react'
import FeedbackRoundedIcon from '@mui/icons-material/FeedbackRounded';
import TerminalRoundedIcon from '@mui/icons-material/TerminalRounded';
import IntegrationInstructionsRoundedIcon from '@mui/icons-material/IntegrationInstructionsRounded';

import { useLinesStore } from 'store/linesStore';
import { useCommandsStore } from 'store/commandsStore';
import { useSelectedWorkflowsStore } from 'store/selectedWorkflowsStore'
import { updateCommandsOrder, deleteCommand } from 'services/commandServices'
import { StaticTabKey } from 'constants/staticCommands'

import Console from 'components/Console'
import ProgramsDrawer from 'components/ProgramsDrawer';
import ProjectTab from 'components/ProjectTab';
import CustomTabsNavigation from 'components/CustomTabsNavigation';
import DefaultDNDList from 'components/DefaultDNDList';
import DrawerTriggerButton from 'components/DrawerTriggerButton'

import TabContentDisplayer from './TabContentDisplayer'
import RunWorkflowButton from './RunWorkflowButton';
import VisualizeDatasetButton from './VisualizeDatasetButton';
import {
  Container,
  SelectedWorkflowsContainer,
} from './styles'

interface IProjectProps {
  projectId: number
}

export default function Project({ projectId }: IProjectProps) {
  const {
    selectedWorkflows,
    setSelectedWorkflows,
    singleSelectedWorkflowId,
    hasSelectedDataset,
    setSingleSelectedWorkflowId,
  } = useSelectedWorkflowsStore((state) => ({
    selectedWorkflows: state.selectedWorkflows,
    setSelectedWorkflows: state.setSelectedWorkflows,
    singleSelectedWorkflowId: state.singleSelectedWorkflowId,
    hasSelectedDataset: state.hasSelectedDataset,
    setSingleSelectedWorkflowId: state.setSingleSelectedWorkflowId,
  }))


  const [isConsoleOpen, setIsConsoleOpen] = useState(false)
  const [isOptionsDrawerOpen, setIsOptionsDrawerOpen] = useState(false)

  const loadLines = useLinesStore((state) => state.loadLines)
  const {
    commands,
    loadCommands,
    setCommands,
    selectedCommandId,
    setSelectedCommandId
  } = useCommandsStore((state) => ({
    commands: state.commands,
    loadCommands: state.loadCommands,
    setCommands: state.setCommands,
    selectedCommandId: state.selectedCommandId,
    setSelectedCommandId: state.setSelectedCommandId,
  }))

  const setUpdateCommandsOrder = (newOrderCommands: orderedCommandsListType) => {
    if (!singleSelectedWorkflowId) return
    if (hasSelectedDataset) return

    const oldOrderCommands = commands
    setCommands([...newOrderCommands])

    const newOrderIds: idsType = newOrderCommands
      .map((command) => command.id)
      // *** "id is number" needed to build
      .filter((id): id is number => typeof id === "number")

    updateCommandsOrder(
      singleSelectedWorkflowId.toString(),
      newOrderIds
    ).then((result) => {
      // ! reverting order changes when face any errors
      if (result == null)
        setCommands([...oldOrderCommands])
    })
  }

  useEffect(() => {
    loadLines(projectId)
  }, [projectId])

  useEffect(() => {
    if (!singleSelectedWorkflowId) return
    loadCommands(singleSelectedWorkflowId)
  }, [singleSelectedWorkflowId])

  return (
    <>
      <Container>
        <ProjectTab />
        <SelectedWorkflowsContainer>
          <CustomTabsNavigation
            tabs={selectedWorkflows}
            setTabs={setSelectedWorkflows}
            selectedTabId={singleSelectedWorkflowId}
            setSelectedTabId={setSingleSelectedWorkflowId}
            CustomDndContext={DefaultDNDList}
            color='white'
          >
            <CustomTabsNavigation
              tabs={hasSelectedDataset ? commands.filter(
                (command) => command.id !== StaticTabKey.Output
              ) : commands}
              setTabs={setUpdateCommandsOrder}
              selectedTabId={selectedCommandId}
              setSelectedTabId={setSelectedCommandId}
              onRemove={(commandId: number | StaticTabKey) =>
                deleteCommand(commandId.toString())
              }
              CustomDndContext={DefaultDNDList}
              color={hasSelectedDataset ? 'secondary' : 'primary'}
              orientation='vertical'
              tabStaticContent={!hasSelectedDataset ?
                <RunWorkflowButton /> :
                <VisualizeDatasetButton />
              }
            >
              <TabContentDisplayer />
            </CustomTabsNavigation>
          </CustomTabsNavigation>
        </SelectedWorkflowsContainer>


        <DrawerTriggerButton
          setIsOpen={setIsConsoleOpen}
          $bottom='16px'
          $left='16px'
        >
          <TerminalRoundedIcon />
        </DrawerTriggerButton>
        <DrawerTriggerButton
          setIsOpen={setIsOptionsDrawerOpen}
          $top='16px'
          $right='16px'
        >
          <IntegrationInstructionsRoundedIcon />
        </DrawerTriggerButton>
      </Container >

      <Console isOpen={isConsoleOpen} setIsOpen={setIsConsoleOpen} />
      <ProgramsDrawer isOpen={isOptionsDrawerOpen} setIsOpen={setIsOptionsDrawerOpen} />
    </>
  )
}
