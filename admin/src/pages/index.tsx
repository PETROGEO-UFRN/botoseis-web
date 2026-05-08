import Grid from '@mui/material/Grid'
import { SimpleTreeView } from '@mui/x-tree-view/SimpleTreeView';
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
      <Grid size={2}>
        <SimpleTreeView
          slots={{
            collapseIcon: ExpandMoreIcon,
            expandIcon: ChevronRightIcon
          }}
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
        </SimpleTreeView>
      </Grid>

      <Grid size={10}>
        <ProgramForm />
      </Grid>
    </Grid>
  )
}
