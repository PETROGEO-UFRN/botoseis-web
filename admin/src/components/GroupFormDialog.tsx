import { useState } from "react"
import type { Dispatch, SetStateAction } from "react"

import Dialog from "@mui/material/Dialog"
import DialogContent from '@mui/material/DialogContent'
import Stack from '@mui/material/Stack';
import TextField from "@mui/material/TextField"
import Button from '@mui/material/Button'
import IconButton from '@mui/material/IconButton'

import CloseRoundedIcon from '@mui/icons-material/CloseRounded';
import WarningAmberIcon from "@mui/icons-material/WarningAmber"

import { useProgramGroups } from "../providers/GroupsProvider"
import { Snackbar, SnackbarContent } from "@mui/material";

interface IGroupFormDialog {
  open: boolean
  setOpen: Dispatch< SetStateAction<boolean> >
}

export default function GroupFormDialog({ open, setOpen }: IGroupFormDialog) {
  const { createProgramGroup } = useProgramGroups()

  const [groupName, setGroupName] = useState("");
  const [groupDescripiton, setGroupDescripiton] = useState("");

  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState("");


  const submitGroup = () => {
    if (!groupName) {
      setSnackbarMessage("Por favor, indique um nome ao grupo")
      return setSnackbarOpen(true)
    }

    const groupData = {
      name: groupName,
      description: groupDescripiton
    }

    setOpen(false)
    resetGroupForm()

    return createProgramGroup(groupData)
  }

  const resetGroupForm = () => {
    setGroupName("")
    setGroupDescripiton("")
  }

  const closeSnackbar = () => {
    setSnackbarOpen(false)
    setSnackbarMessage("")
  }

  return (
    <Dialog
      open={open}
      onClose={() => setOpen(false)}
      fullWidth
    >
      <DialogContent>
        <IconButton
          onClick={() => setOpen(false)}
          sx={{
            position: "absolute",
            top: "16px",
            right: "16px",
          }}
        >
          <CloseRoundedIcon fontSize="large" color="error" />
        </IconButton>

        <Stack
          component="form"
          onSubmit={(event) => {
            event.preventDefault()
            submitGroup()
            // setOpen(false)
          }}
          sx={{ gap: "32px", marginTop: "64px" }}
        >
          <TextField
            label="Nome do grupo"
            value={groupName}
            onChange={(event) => setGroupName(event.target.value)}
          />
          <TextField
            label="Descrição do grupo (opcional)"
            value={groupDescripiton}
            onChange={(event) => setGroupDescripiton(event.target.value)}
          />

          <Button
            type="submit"
            variant="contained"
          >
            Salvar Novo Grupo
          </Button>
        </Stack>
        <Snackbar
          open={snackbarOpen}
          anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
          autoHideDuration={3000}
          onClose={closeSnackbar}
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
      </DialogContent>
    </Dialog>
  )
}
