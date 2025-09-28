import { useShallow } from 'zustand/react/shallow';
import { TreeItem } from '@mui/x-tree-view/TreeItem';
import Button from '@mui/material/Button';
import NoteAddRoundedIcon from '@mui/icons-material/NoteAddRounded';

import { TreeItemLabelWithActions } from 'shared-ui';

import { defaultWorkflowName } from 'constants/defaults';
import { useLinesStore } from 'store/linesStore';

interface IWorkflowsFolderProps {
  lineId: number
  data: Array<IResumedWorkflow>
}

const entityType = 'workflow'

export default function WorkflowsFolder({
  lineId,
  data,
}: IWorkflowsFolderProps) {
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
      itemId={`${lineId}-${entityType}s-folder`}
      label={`${entityType}s`}
    >
      {data.map((workflow) => (
        <TreeItem
          key={workflow.id}
          itemId={`${entityType}-${workflow.id}`}
          label={
            <TreeItemLabelWithActions
              labelText={workflow.name}
              onRemove={() => removeWorkflowFromLine(lineId, workflow.id)}
              onUpdate={(newName) => updateWorkflowName(lineId, workflow.id, newName)}
            />
          }
        />
      ))}

      <Button
        onClick={() => pushNewWorkflowToLine(
          lineId,
          generateNextWorkflowName()
        )}
        fullWidth
      >
        <NoteAddRoundedIcon />
        New Workflow
      </Button>
    </TreeItem>
  )
}
