import { useEffect } from 'react'
import { useLocation } from "@tanstack/react-location"
import { useShallow } from 'zustand/react/shallow'
import { TreeItem } from '@mui/x-tree-view/TreeItem'
import { TreeItemLabelWithActions } from 'shared-ui'

import { useTablesStore } from 'store/tablesStore'

interface ITablesFolder {
  lineId: number
}

export default function TablesFolder({ lineId }: ITablesFolder) {
  const location = useLocation()
  const projectId = Number(location.current.pathname.split('/')[2])
  const {
    tables,
    loadTables,
  } = useTablesStore(useShallow((state) => ({
    tables: state.tables,
    loadTables: state.loadTables,
  })))

  useEffect(() => {
    loadTables(projectId)
  }, [projectId])

  return (
    <TreeItem
      itemId={`${lineId}-tables-folder`}
      label="Tables"
    >
      {tables.map(table => (
        <TreeItem
          key={table.id}
          itemId={`table-${table.id}`}
          label={
            <TreeItemLabelWithActions
              labelText={table.name}
            />
          }
        >
        </TreeItem>
      ))}
    </TreeItem>
  );
}
