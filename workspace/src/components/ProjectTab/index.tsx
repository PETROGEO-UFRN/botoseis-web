import { useState } from 'react'
import type { SyntheticEvent } from 'react'
import { useTimeout } from 'react-use';
import { useShallow } from 'zustand/react/shallow'

import { SimpleTreeView } from '@mui/x-tree-view/SimpleTreeView';
import { TreeItem } from '@mui/x-tree-view/TreeItem';
import ExpandMoreIcon from '@mui/icons-material/ExpandMoreRounded';
import ChevronRightIcon from '@mui/icons-material/ChevronRightRounded';

import { TreeItemLabelWithActions } from 'shared-ui';

import { useLinesStore } from 'store/linesStore';
import { useSelectedWorkflowsStore } from 'store/selectedWorkflowsStore';
import LineChildrenFolder from './LineChildrenFolder'
import DataSetsFolder from './DataSetsFolder'
import MenuActions from './MenuActions';

import { Container } from "./styles"

export default function ProjectTab() {
  const {
    lines,
    removeLine,
    updateLineName,
  } = useLinesStore(useShallow((state) => ({
    lines: state.lines,
    removeLine: state.removeLine,
    updateLineName: state.updateLineName,
  })))
  const selectWorkflow = useSelectedWorkflowsStore(useShallow((state) => (
    state.selectWorkflow
  )))

  const [expandedItems, setExpandedItems] = useState<string[]>([]);
  const [selectedItems, setSelectedItems] = useState<string>("");
  const [isAllowToSelect, _, resetAllowToSelectTimer] = useTimeout(1000);

  const handleToggle = (_: SyntheticEvent | null, itemId: string[] | null) => {
    if (!itemId)
      return
    setExpandedItems(itemId);
  };

  const handleSelect = (_: SyntheticEvent | null, itemId: string | null) => {
    if (!isAllowToSelect())
      return
    if (!itemId)
      return
    resetAllowToSelectTimer()

    const isWorkflow = itemId.startsWith("workflow")
    const isDataset = itemId.startsWith("dataset")


    if (!(isWorkflow || isDataset))
      return
    const [key, id, name] = itemId.split("-")

    if (key !== "workflow" || !id || !name)
      return

    selectWorkflow(Number(id), () => setSelectedItems(itemId))
  }

  return (
    <Container>
      <SimpleTreeView
        slots={{
          collapseIcon: ExpandMoreIcon,
          expandIcon: ChevronRightIcon
        }}
        expandedItems={expandedItems}
        selectedItems={selectedItems}
        onExpandedItemsChange={handleToggle}
        onSelectedItemsChange={handleSelect}
      >
        <MenuActions />
        {Boolean(lines.length) && lines.map((line) => (
          <TreeItem
            key={line.id}
            itemId={`line-${line.id}`}
            label={
              <TreeItemLabelWithActions
                labelText={line.name}
                onRemove={() => removeLine(line.id)}
                onUpdate={(newName) => updateLineName(line.id, newName)}
              />
            }
          >
            <LineChildrenFolder
              lineId={line.id}
              entityType='workflow'
              data={line.workflows}
            />

            <DataSetsFolder line={line} />
          </TreeItem>
        ))}
      </SimpleTreeView>
    </Container>
  )
}
