import { useEffect, useState } from 'react';
import { TreeItem } from '@mui/x-tree-view/TreeItem';

import api from 'services/api';

interface IDatasetWorkflows {
  workflowId: number
}

export default function DatasetWorkflows({ workflowId }: IDatasetWorkflows) {
  const [datasets, setDatasets] = useState<Array<IWorkflow>>([])

  useEffect(() => {
    api.get<Array<IWorkflow>>(`/dataset/list/${workflowId}`).then((response) => {
      setDatasets(response.data)
    })
  }, [])

  return (
    <>
      {datasets.map((dataset) => (
        <TreeItem
          itemId={`workflow-${dataset.id}-from-dataset-from-${workflowId}`}
          label={dataset.output_name ? dataset.output_name : `dataset-${dataset.id}`}
          key={dataset.id}
        />
      ))}
    </>
  )
}