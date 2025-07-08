import { useShallow } from 'zustand/react/shallow';
import { TreeItem } from '@mui/x-tree-view/TreeItem';
import Button from '@mui/material/Button';
import NoteAddRoundedIcon from '@mui/icons-material/NoteAddRounded';

import { TreeItemLabelWithActions } from 'shared-ui';

import { defaultWorkflowName } from 'constants/defaults';
import { useLinesStore } from 'store/linesStore';

interface ILineChildrenFolderProps {
  lineId: number
  entityType: "workflow" | "dataset"
  data: Array<IResumedWorkflow>
}

export default function LineChildrenFolder({
  lineId,
  entityType,
  data,
}: ILineChildrenFolderProps) {
  const {
    pushNewWorkflowToLine,
    updateWorkflowName,
    removeWorkflowFromLine,
  } = useLinesStore(useShallow((state) => ({
    pushNewWorkflowToLine: state.pushNewWorkflowToLine,
    updateWorkflowName: state.updateWorkflowName,
    removeWorkflowFromLine: state.removeWorkflowFromLine
  })))

  const generateNextWorkflowName = () => {
    if (data.length < 1)
      return defaultWorkflowName

    return (
      `${defaultWorkflowName} (${data.length + 1})`
    )
  }

  return (
    <TreeItem
      itemId={`from-${lineId}-${entityType}`}
      label={`${entityType}s`}
    >
      {data.map((workflow) => (
        <TreeItem
          key={`${entityType}-${workflow.id}`}
          itemId={`${entityType}-${workflow.id}-${workflow.name}`}
          label={
            <TreeItemLabelWithActions
              labelText={workflow.name}
              onRemove={() => removeWorkflowFromLine(lineId, workflow.id)}
              onUpdate={(newName) => updateWorkflowName(lineId, workflow.id, newName)}
            />
          }
        />
      ))}
      {entityType == "workflow" && (
        <Button
          onClick={() => pushNewWorkflowToLine(
            lineId,
            generateNextWorkflowName()
          )}
        >
          <NoteAddRoundedIcon />
          New Workflow
        </Button>
      )}
    </TreeItem>
  )
}
