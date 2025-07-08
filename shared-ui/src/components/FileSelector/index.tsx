import { useState } from "react"

import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import Button from "@mui/material/Button"

import FileUploadDialog from "../FileUploadDialog"
import { uploadNewFileType } from "../FileUploadDialog"

interface IFileSelectorProps {
  fileLinks: Array<IfileLink>
  selectedFileLinkId: number | undefined
  onSubmitFileLinkUpdate: (fileLinkId: number) => void
  uploadNewFile: uploadNewFileType
}

export default function FileSelector({
  fileLinks,
  selectedFileLinkId,
  onSubmitFileLinkUpdate,
  uploadNewFile,
}: IFileSelectorProps) {
  const [isFileUploadDialogOpen, setIsFileUploadDialogOpen] = useState<boolean>(false)

  return (
    <>
      <Select
        value={selectedFileLinkId}
        onChange={(event) => onSubmitFileLinkUpdate(event.target.value)}
        variant="outlined"
      >
        {fileLinks.map((fileLink) =>
          <MenuItem key={fileLink.id} value={fileLink.id}>
            {fileLink.name}
          </MenuItem>
        )}

        <Button
          onClick={() => setIsFileUploadDialogOpen(true)}
        >
          Upload de novo arquivo
        </Button>
      </Select>

      <FileUploadDialog
        open={isFileUploadDialogOpen}
        setOpen={setIsFileUploadDialogOpen}
        uploadNewFile={uploadNewFile}
      />
    </>
  )
}
