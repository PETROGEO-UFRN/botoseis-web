import type { Key } from 'react'

import Typography from '@mui/material/Typography'
import List from '@mui/material/List'
import AccordionSummary from '@mui/material/AccordionSummary'
import AccordionDetails from '@mui/material/AccordionDetails'
import Button from '@mui/material/Button'
import Tooltip from '@mui/material/Tooltip'

import KeyboardBackspaceRoundedIcon from '@mui/icons-material/KeyboardBackspaceRounded'
import ExpandMoreRoundedIcon from '@mui/icons-material/ExpandMoreRounded'
import QuestionMarkIcon from '@mui/icons-material/QuestionMark'

import {
  GroupsListBox,
  PackageAccordionSummary,
  Title,
  CustomAccordion,
  CustomListItem
} from './styles'

interface IProgramsGroupsAccordionProps<ProgramIDType extends Key> {
  packageTitle: string,
  programsGroups: Array<IProgramsGroup<ProgramIDType>>,
  addProgramToCurrentWorkflow: (
    name: string,
    program_id: ProgramIDType
  ) => void,
}

export default function ProgramsGroupsAccordion<ProgramIDType extends Key>({
  packageTitle,
  programsGroups,
  addProgramToCurrentWorkflow,
}: IProgramsGroupsAccordionProps<ProgramIDType>) {
  return (
    <CustomAccordion>
      <PackageAccordionSummary expandIcon={<ExpandMoreRoundedIcon />}>
        <Title variant='h5'>
          {packageTitle}
        </Title>
      </PackageAccordionSummary>

      <AccordionDetails>
        <GroupsListBox>
          {programsGroups.map((group) => (
            <CustomAccordion
              key={group.id}
              disableGutters
            >
              <AccordionSummary expandIcon={<ExpandMoreRoundedIcon />}>
                <Typography
                  variant='subtitle1'
                  fontWeight="700"
                >
                  {group.name.toUpperCase()}
                </Typography>
              </AccordionSummary>

              <AccordionDetails>
                <List
                  dense
                  disablePadding
                >
                  {group.programs.map((program) => (
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
                  ))}
                </List>
              </AccordionDetails>
            </CustomAccordion>
          ))}
        </GroupsListBox>
      </AccordionDetails>
    </CustomAccordion>
  )
}
