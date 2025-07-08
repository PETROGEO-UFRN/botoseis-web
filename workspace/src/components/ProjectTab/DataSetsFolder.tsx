import { TreeItem } from '@mui/x-tree-view/TreeItem';

import DatasetWorkflows from './DatasetWorkflows'

interface IDataSetsFolderProps {
  line: ILine
}

export default function DataSetsFolder({ line }: IDataSetsFolderProps) {
  return (
    <TreeItem
      itemId={`from-${line.id}-datasets-folder`}
      label={`Datasets`}
    >
      {line.workflows.map((workflow) => (
        <TreeItem
          itemId={`from-${line.id}-datasets-${workflow.id}`}
          label={`dataset->${workflow.name}`}
          key={workflow.id}
        >
          <DatasetWorkflows workflowId={workflow.id} />
        </TreeItem>
      ))}
    </TreeItem>
  )
}