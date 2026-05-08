import type { ReactNode } from 'react';

import { TreeItem } from '@mui/x-tree-view/TreeItem';
import Button from '@mui/material/Button';

import { TreeItemLabelWithActions } from 'shared-ui';

import { useSelectedProgramCommand } from '../providers/SelectedProgramProvider';

interface ITreeItemWithActionProps {
  children: ReactNode
  itemId: string
  labelText: string
  deleteAction(): void
}

export default function TreeItemWithAction({
  children,
  itemId,
  labelText,
  deleteAction
}: ITreeItemWithActionProps) {
  const { setSelectedProgram } = useSelectedProgramCommand()

  return (
    <TreeItem
      itemId={itemId}
      label={
        <TreeItemLabelWithActions
          labelText={labelText}
          onRemove={deleteAction}
        />
      }
    >
      <Button variant="contained" onClick={() => setSelectedProgram(null)}>
        Novo programa
      </Button>
      {children}
    </TreeItem>
  )
}
