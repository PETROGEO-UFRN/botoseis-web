import { useEffect, useState } from 'react';
import { TreeItem } from '@mui/x-tree-view/TreeItem';

import api from 'services/api';

interface IDatasetWorkflows {
  workflowId: number
}

export default function DatasetWorkflows({ workflowId }: IDatasetWorkflows) {
  const [datasets, setDatasets] = useState<Array<IWorkflow>>([])

  useEffect(() => {
    // !turn into service
    api.get<Array<IWorkflow>>(`/dataset/list/${workflowId}`).then((response) => {
      setDatasets(response.data)
    })
    // !trigger also when something related to run-workflow button for this ID
  }, [workflowId])

  return (
    <>
      {datasets.map((dataset) => (
        <TreeItem
          itemId={`workflow-${workflowId}`}
          label={dataset.output_name ? dataset.output_name : `dataset-${dataset.id}`}
          key={dataset.id}
        />
      ))}
    </>
  )
}
