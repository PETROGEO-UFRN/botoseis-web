import Grid from '@mui/material/Grid'
import { TreeView } from '@mui/x-tree-view/TreeView';
import { TreeItem } from '@mui/x-tree-view/TreeItem';

import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';

import ProgramForm from '../components/ProgramForm';
import TreeItemWithAction from '../components/TreeItemWithAction';
import { useProgramGroups } from '../providers/GroupsProvider'
import { useSelectedProgramCommand } from '../providers/SelectedProgramProvider'

export default function Home() {
  const { programGroups, deleteProgramGroup } = useProgramGroups()
  const { setSelectedProgram } = useSelectedProgramCommand()

  return (
    <Grid container sx={{ height: "100%" }}>
      <Grid item xs={2}>
        <TreeView
          defaultCollapseIcon={<ExpandMoreIcon />}
          defaultExpandIcon={<ChevronRightIcon />}
        >
          {programGroups.map(group => (
            <TreeItemWithAction
              key={`group-${group.id}`}
              itemId={`group-${group.id}`}
              labelText={group.name}
              deleteAction={() => deleteProgramGroup(group.id)}
            >
              {group.programs.map(program => (
                <TreeItem
                  key={`${group.id}-program-${program.id}`}
                  itemId={`${group.id}-program-${program.id}`}
                  label={program.name}
                  onClick={() => setSelectedProgram(program)}
                />
              ))}
            </TreeItemWithAction>
          ))}
        </TreeView>
      </Grid>

      <Grid item xs={10}>
        <ProgramForm />
      </Grid>
    </Grid>
  )
}
