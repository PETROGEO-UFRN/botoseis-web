import { useEffect, useState } from 'react'

import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField'
import Select from '@mui/material/Select'
import MenuItem from '@mui/material/MenuItem'
import Button from '@mui/material/Button';
import InputLabel from '@mui/material/InputLabel';
import FormControl from '@mui/material/FormControl';
import Snackbar from '@mui/material/Snackbar';
import SnackbarContent from '@mui/material/SnackbarContent';
import WarningAmberIcon from "@mui/icons-material/WarningAmber"

import ParameterForm from './ParameterForm';
import GroupFormDialog from './GroupFormDialog';
import ProgramCommandOrFileInput from './ProgramCommandOrFileInput';
import { createNewProgram, updateProgram, deleteProgram } from '../services/programServices'
import { useProgramGroups } from '../providers/GroupsProvider'
import { useSelectedProgramCommand } from '../providers/SelectedProgramProvider'
import { Dialog, DialogActions, DialogContent, DialogTitle, Typography } from '@mui/material';


export default function ProgramForm() {
  const { programGroups, addNewProgramOnGroup, updateProgramOnGroup } = useProgramGroups()
  const { selectedProgram } = useSelectedProgramCommand()

  const [openGroupFormDialog, setOpenGroupFormDialog] = useState<boolean>(false)
  const [openConfirmDialog, setOpenConfirmDialog] = useState(false)

  const [programName, setProgramName] = useState("")
  const [programDescription, setProgramDescription] = useState("")
  const [programPath, setProgramPath] = useState("")
  const [groupId, setGroupId] = useState<number | null>(null)

  const [customProgram, setCustomProgram] = useState<FileList | null>(null)

  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState("");

  const submitProgram = () => {
    if (!programName || !programDescription || !programPath) {
      setSnackbarMessage("Por favor, preencha todos os campos")
      return setSnackbarOpen(true)
    }
    if (!groupId) {
      setSnackbarMessage("Por favor, selecione um grupo")
      return setSnackbarOpen(true)
    }

    // update state on setProgramGroups
    const programData = {
      name: programName,
      description: programDescription,
      path_to_executable_file: programPath,
      groupId: groupId
    }

    if(selectedProgram)
      return updateProgram(
        selectedProgram.id,
        customProgram,
        programData
      ).then((updatedProgram) => updatedProgram && updateProgramOnGroup(updatedProgram))

    resetProgramForm()

    return createNewProgram(
      groupId,
      customProgram,
      programData
    ).then((newProgram) => newProgram && addNewProgramOnGroup(newProgram))

  }

  const resetProgramForm = () => {
    setProgramName("")
    setProgramDescription("")
    setProgramPath("")
    setGroupId(null)
    setCustomProgram(null)
  }

  const closeSnackbar = () => {
    setSnackbarOpen(false)
    setSnackbarMessage("")
  }

  const confirmDelete = () => {
    if (selectedProgram) {
      deleteProgram(selectedProgram.id)
      setOpenConfirmDialog(false)
      resetProgramForm()
    }
  }

  useEffect(() => {
    if (!selectedProgram) {
      setProgramName("")
      setProgramDescription("")
      setProgramPath("")
      setGroupId(null)
      return
    }
    setProgramName(selectedProgram.name)
    setProgramDescription(selectedProgram.description)
    setProgramPath(selectedProgram.path_to_executable_file)
    setGroupId(selectedProgram.groupId)
  }, [selectedProgram])

  return (
    <Stack direction="column" sx={{ gap: "32px", padding: "32px" }} >
      <TextField
        label="Nome do Programa"
        value={programName}
        onChange={(event) => setProgramName(event.target.value)}
      />
      <TextField
        label="Descrição do Programa"
        value={programDescription}
        onChange={(event) => setProgramDescription(event.target.value)}
      />
      {/* todo: add checkbox to alow upload a binary file or use a command */}
      <ProgramCommandOrFileInput
        programPath={programPath}
        setProgramPath={setProgramPath}
        setCustomProgram={setCustomProgram}
      />
      <Stack direction="row"  >
        <FormControl fullWidth>
          <InputLabel id="groupId-select">Grupo</InputLabel>
          <Select
            label="Grupo"
            value={groupId}
            onChange={(event) => setGroupId(event.target.value as number)}
            labelId="groupId-select"
          >
            {programGroups.map(group => (
              <MenuItem key={group.id} value={group.id}>
                {group.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <Button onClick={() => setOpenGroupFormDialog(true)}>
          Novo Grupo
        </Button>
      </Stack>

      <Stack direction="row" sx={{ gap: "8px" }} >
        <Button variant="contained" onClick={submitProgram}>
          Salvar {!selectedProgram && " Novo Programa"}
        </Button>
        {selectedProgram && (
          <Button onClick={() => setOpenConfirmDialog(true)}>
            Apagar programa
          </Button>
        )}
      </Stack>
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={3000}
        onClose={closeSnackbar}
        anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
      >
        <SnackbarContent
          sx={{
            backgroundColor: "#ff9800",
            color: "#fff",
            display: "flex",
            alignItems: "center",
            padding: "8px 16px",
          }}
          message={
            <span style={{ display: "flex", alignItems: "center" }}>
              <WarningAmberIcon sx={{ marginRight: "8px" }} />
              {snackbarMessage}
            </span>
          }
        />
      </Snackbar>
      <Dialog
        open={openConfirmDialog}
        onClose={() => setOpenConfirmDialog(false)}
        aria-labelledby='confirm-delete-dialog'
      >
        <DialogTitle id="confirm-delete-dialog">Sim</DialogTitle>
        <DialogContent>
          <Typography>
            Tem certeza que deseja deletar o programa "{selectedProgram?.name}"?
            A ação não pode ser desfeita.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenConfirmDialog(false)}>Cancelar</Button>
          <Button variant="contained" color="error" onClick={confirmDelete}>
            Deletar
          </Button>
        </DialogActions>
      </Dialog>


      <ParameterForm />

      <GroupFormDialog
        open={openGroupFormDialog}
        setOpen={setOpenGroupFormDialog}
      />
    </Stack>
  )
}
