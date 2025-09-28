import { useState } from "react"

import FormControl from "@mui/material/FormControl"
import FormLabel from "@mui/material/FormLabel"
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
  label?: string
  size?: "small" | "medium"
}

export default function FileSelector({
  fileLinks,
  selectedFileLinkId,
  onSubmitFileLinkUpdate,
  uploadNewFile,

  label = "Select File",
  size = "medium",
}: IFileSelectorProps) {
  const [isFileUploadDialogOpen, setIsFileUploadDialogOpen] = useState<boolean>(false)

  return (
    <FormControl>
      <FormLabel>
        {label}
      </FormLabel>
      <Select
        value={selectedFileLinkId}
        onChange={(event) => onSubmitFileLinkUpdate(event.target.value)}
        size={size}
      >
        {fileLinks.map((fileLink) =>
          <MenuItem key={fileLink.id} value={fileLink.id}>
            {fileLink.name}
          </MenuItem>
        )}

        <Button
          onClick={() => setIsFileUploadDialogOpen(true)}
        >
          Upload new file
        </Button>
      </Select>

      <FileUploadDialog
        open={isFileUploadDialogOpen}
        setOpen={setIsFileUploadDialogOpen}
        uploadNewFile={uploadNewFile}
      />
    </FormControl>
  )
}
