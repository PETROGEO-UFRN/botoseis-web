import { useState } from 'react';
import type { FormEvent } from 'react';

import Dialog from "@mui/material/Dialog";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import TextField from "@mui/material/TextField";
import Button from '@mui/material/Button';

import AddRoundedIcon from "@mui/icons-material/AddRounded"

import { createNewProject } from 'services/projectServices';

import { AddProjectButton } from './styles'

interface INewProjectDialogProps {
  pushNewProject(newProject: IProject): void
}

export default function NewProjectDialog({ pushNewProject }: INewProjectDialogProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [projectName, setProjectName] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const closeDialog = () => {
    setIsOpen(false)
  }

  const submitNewProject = (event: FormEvent) => {
    event.preventDefault()
    setIsLoading(true)
    createNewProject(projectName).then(
      (newProject) => newProject && pushNewProject(newProject)
    )
    setIsLoading(false)
    closeDialog()
  }

  return (
    <>
      <Dialog
        open={isOpen}
        onClose={closeDialog}
        component="form"
        onSubmit={submitNewProject}
      >
        <DialogContent>
          <TextField
            label="Nome do projeto"
            value={projectName}
            onChange={(event) => setProjectName(event.target.value)}
          />
        </DialogContent>

        <DialogActions>
          <Button onClick={closeDialog} >
            Cancelar
          </Button>

          <Button
            type='submit'
            loading={isLoading}
          >
            Salvar
          </Button>
        </DialogActions>
      </Dialog>

      <AddProjectButton
        color='primary'
        onClick={() => setIsOpen(true)}
      >
        <AddRoundedIcon />
      </AddProjectButton>
    </>
  )
}