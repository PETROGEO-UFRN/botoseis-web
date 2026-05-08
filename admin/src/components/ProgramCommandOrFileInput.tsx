import { useCallback, useEffect, useState } from 'react';
import type { Dispatch, SetStateAction } from 'react';

import { useDebounce } from 'use-debounce';
import Stack from '@mui/material/Stack';
import FormControlLabel from '@mui/material/FormControlLabel';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Switch from '@mui/material/Switch';

import CloudUploadIcon from '@mui/icons-material/CloudUploadRounded';


interface IProgramCommandOrFileInputProps {
  programPath: string
  setProgramPath: Dispatch< SetStateAction<string> >
  setCustomProgram: Dispatch< SetStateAction<FileList | null> >
}

export default function  ProgramCommandOrFileInput({
  programPath,
  setProgramPath,
  setCustomProgram
}: IProgramCommandOrFileInputProps) {
  const [hasCustomFile, setHasCustomFile] = useState(false)
  const [hasCustomFileDebounced] = useDebounce(hasCustomFile, 2000)

  const setProgramPathCallback = useCallback(setProgramPath, [setProgramPath])

  useEffect(() => {
    if(hasCustomFileDebounced)
      setProgramPathCallback("")
  }, [hasCustomFileDebounced, setProgramPathCallback])

  return (
    <Stack
      direction="row"
      spacing={2}
      sx={{alignItems: "center"}}
    >
      {hasCustomFile ? (
        <Button
          component="label"
          role={undefined}
          variant="contained"
          tabIndex={-1}
          startIcon={<CloudUploadIcon />}
        >
          Upload do programa
          <input
            type="file"
            onChange={(event) => {
              if(event.target.files)
                setCustomProgram(event.target.files)
            }}
            style={{
              clip: 'rect(0 0 0 0)',
              overflow: 'hidden',
              position: 'absolute',
              bottom: 0,
              left: 0,
            }}
          />
        </Button>
      ) : (
        <TextField
          label="Comando ou caminho do Programa"
          value={programPath}
          onChange={(event) => setProgramPath(event.target.value)}
          fullWidth
        />
      )}
      <FormControlLabel
        control={
          <Switch
            checked={hasCustomFile}
            onChange={(event) => setHasCustomFile(event.target.checked)}
          />
        }
        label={hasCustomFile ? "Upload Customizado" : "Comando"}
        sx={{width: "fit-content"}}
      />
    </Stack>
  )
}
