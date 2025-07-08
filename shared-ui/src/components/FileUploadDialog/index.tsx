import { useState } from "react"
import type { Dispatch, SetStateAction } from "react"

import Dialog from '@mui/material/Dialog'
import DialogTitle from '@mui/material/DialogTitle'
import DialogContent from '@mui/material/DialogContent'
import DialogActions from '@mui/material/DialogActions'
import Button from '@mui/material/Button'

export type uploadNewFileType = (newFile: File, formData: FormData) => void

interface IFileUploadDialogProps {
  open: boolean
  setOpen: Dispatch<SetStateAction<boolean>>
  uploadNewFile: uploadNewFileType
}

export default function FileUploadDialog({
  open,
  setOpen,
  uploadNewFile,
}: IFileUploadDialogProps) {
  const [file, setFile] = useState<any>(null)

  const saveNewFile = () => {
    if (!file)
      return

    const formData = new FormData();
    formData.append('file', file);

    uploadNewFile(file, formData)
    setOpen(false)
  }

  return (
    <Dialog
      open={open}
      onClose={() => setOpen(false)}
    >
      <DialogTitle>
        Upload novo arquivo .su
      </DialogTitle>

      <DialogContent>
        <input
          type="file"
          onChange={(event) => event.target.files && setFile(event.target.files[0])}
        />
      </DialogContent>

      <DialogActions>
        <Button
          variant="contained"
          onClick={saveNewFile}
        >
          Salvar Novo Arquivo
        </Button>
      </DialogActions>
    </Dialog>
  )
}
