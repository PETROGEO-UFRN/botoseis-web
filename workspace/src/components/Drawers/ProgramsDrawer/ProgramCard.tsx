import { memo } from 'react'
import type { Key } from 'react'

import Button from '@mui/material/Button'
import Tooltip from '@mui/material/Tooltip'
import Typography from '@mui/material/Typography'

import KeyboardBackspaceRoundedIcon from '@mui/icons-material/KeyboardBackspaceRounded'
import QuestionMarkIcon from '@mui/icons-material/QuestionMark'

import {
  CustomListItem,
} from './styles'

export type addProgramToCurrentWorkflowType<ProgramIDType> = (
  name: string,
  program_id: ProgramIDType
) => void

interface IProgramCard<ProgramIDType extends Key> {
  program: IGenericProgram<ProgramIDType>
  addProgramToCurrentWorkflow: addProgramToCurrentWorkflowType<ProgramIDType>
}

function ProgramCard<ProgramIDType extends Key>({
  program,
  addProgramToCurrentWorkflow,
}: IProgramCard<ProgramIDType>) {
  return (
    <CustomListItem
      key={program.id}
      disableGutters
    >
      <Button
        onClick={() => addProgramToCurrentWorkflow(
          program.path_to_executable_file,
          program.id,
        )}
        variant='text'
        startIcon={<KeyboardBackspaceRoundedIcon />}
      >
        <Typography
          variant='body1'
        >
          {program.name}
        </Typography>
      </Button>

      <Tooltip
        title={program.description}
        placement='top'
        arrow
      >
        <QuestionMarkIcon
          color='primary'
          fontSize='small'
        />
      </Tooltip>
    </CustomListItem>
  )
}

export default memo(ProgramCard) as typeof ProgramCard
