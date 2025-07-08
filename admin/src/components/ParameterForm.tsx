import { useState, useEffect } from 'react'

import { useDebounce } from 'use-debounce';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField'
import FormControlLabel from '@mui/material/FormControlLabel'
import Switch from '@mui/material/Switch'
import Typography from '@mui/material/Typography'
import Button from '@mui/material/Button';
import Snackbar from '@mui/material/Snackbar';
import SnackbarContent from '@mui/material/SnackbarContent';
import CheckCircleIcon from "@mui/icons-material/CheckCircle"

import { DeleteButton } from "shared-ui"

import {
  getParameters,
  createNewParameter,
  updateParameter,
  deleteParameter
} from '../services/parameterServices';
import { useSelectedProgramCommand } from '../providers/SelectedProgramProvider';

export default function ParameterForm() {
  const { selectedProgram } = useSelectedProgramCommand()

  const [parameters, setParamenters] = useState<Array<IParameter>>([])
  const [parametersDebounced] = useDebounce(parameters, 2000)
  const [feedbackSnackbar, setFeedbackSnackbar] = useState(false)

  interface IupdateParameterFieldProps {
    index: number
    key: "name" | "input_type" | "description" | "example" | "isRequired"
    newValue?: string
    newIsRequiredValue?: boolean
  }

  const updateParameterField = ({ index, key, newValue, newIsRequiredValue }: IupdateParameterFieldProps) => {
    const newParameters = [...parameters]
    if (key == "isRequired") newParameters[index][key] = Boolean(newIsRequiredValue)
    else newParameters[index][key] = String(newValue)

    newParameters[index].hasChanges = true
    setParamenters(newParameters)
  }

  const triggerSnackbar = () => {
    setFeedbackSnackbar(true);
    setTimeout(() => {
      setFeedbackSnackbar(false);
    }, 2000);
  };

  useEffect(() => {
    if (!selectedProgram) return setParamenters([])
    getParameters(selectedProgram.id).then(programParameters => setParamenters(programParameters))
  }, [selectedProgram])

  useEffect(() => {
    let hasUpdates = false;
    parametersDebounced.forEach((paremeter) => {
      if(paremeter.hasChanges) {
        console.log("achou um parametro com mudanças")
        updateParameter(paremeter)
        hasUpdates = true;
      }
    })
    if (hasUpdates) {
      triggerSnackbar();
    }
  }, [parametersDebounced])

  return selectedProgram && (
    <>
    <Typography variant="h4">
      Parametros
    </Typography>
    {parameters.map((parameter, index) => (
      <Stack
        direction="row"
        key={index}
        spacing={2}
        sx={{alignItems: "center"}}
      >
        <TextField
          label="Nome do Parametro"
          value={parameter.name}
          onChange={(event) => updateParameterField({index, key: "name", newValue: event.target.value})}
        />
        <TextField
          label="Tipo do parametro"
          value={parameter.input_type}
          onChange={(event) => updateParameterField({index, key: "input_type", newValue: event.target.value})}
        />
        <TextField
          label="Descrição do Parametro"
          value={parameter.description}
          onChange={(event) => updateParameterField({index, key: "description", newValue: event.target.value})}
          fullWidth
        />
        <TextField
          label="Exemplo de uso"
          value={parameter.example}
          onChange={(event) => updateParameterField({index, key: "example", newValue: event.target.value})}
          fullWidth
        />
        <FormControlLabel
          control={
            <Switch
              checked={parameter.isRequired}
              onChange={(event) => updateParameterField({index, key: "isRequired", newIsRequiredValue: event.target.checked})}
            />
          }
          label={parameter.isRequired ? "Obrigatorio" : "Opcional"}
          sx={{width: "192px"}}
        />

        {/* Snackbar */}
        <Snackbar open={feedbackSnackbar} anchorOrigin={{ vertical: "bottom", horizontal: "center" }}>
          <SnackbarContent
            sx={{
              backgroundColor: "#4caf50",
              display: "flex",
              alignItems: "center",
            }}
            message={
              <span style={{ display: "flex", alignItems: "center" }}>
                <CheckCircleIcon sx={{ marginRight: "8px" }} />
                Parâmetros salvos com sucesso
              </span>
            }
          />
        </Snackbar>

        <DeleteButton
          onRemove={() => deleteParameter(parameter.id).then(() => {
            const newParameters = [...parameters]
            newParameters.splice(index, 1)
            setParamenters(newParameters)
          })}
        />
      </Stack>
    ))}

    <Button
      variant="contained"
      onClick={() => createNewParameter(selectedProgram.id).then(
        (newParameter) => newParameter && setParamenters([...parameters, newParameter])
      )}
    >
      Novo Parametro
    </Button>
    </>
  )
}
