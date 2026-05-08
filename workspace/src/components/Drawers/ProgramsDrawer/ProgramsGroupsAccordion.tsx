import type { Key, Dispatch, SetStateAction } from 'react'

import List from '@mui/material/List'

import Typography from '@mui/material/Typography'
import AccordionSummary from '@mui/material/AccordionSummary'
import AccordionDetails from '@mui/material/AccordionDetails'

import ExpandMoreRoundedIcon from '@mui/icons-material/ExpandMoreRounded'

import ProgramCard from './ProgramCard'
import type { addProgramToCurrentWorkflowType } from './ProgramCard'

import {
  PackageAccordionSummary,
  Title,
  CustomAccordion,
} from './styles'

interface IProgramsGroupsAccordionProps<ProgramIDType extends Key> {
  isExpanded: boolean,
  onChange: Dispatch<SetStateAction<boolean>>,
  packageTitle: string,
  programsGroups: Array<IProgramsGroup<ProgramIDType>>,
  addProgramToCurrentWorkflow: addProgramToCurrentWorkflowType<ProgramIDType>
}

export default function ProgramsGroupsAccordion<ProgramIDType extends Key>({
  isExpanded,
  onChange,
  packageTitle,
  programsGroups,
  addProgramToCurrentWorkflow,
}: IProgramsGroupsAccordionProps<ProgramIDType>) {
  return (
    <CustomAccordion
      expanded={isExpanded}
      onChange={() => onChange(!isExpanded)}
    >
      <PackageAccordionSummary expandIcon={<ExpandMoreRoundedIcon />}>
        <Title variant='h5'>
          {packageTitle}
        </Title>
      </PackageAccordionSummary>

      <AccordionDetails>
        {programsGroups.map((group) => (
          <CustomAccordion
            key={group.id}
            slotProps={{ transition: { unmountOnExit: true } }}
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
                  <ProgramCard<ProgramIDType>
                    program={program}
                    addProgramToCurrentWorkflow={addProgramToCurrentWorkflow}
                  />
                ))}
              </List>
            </AccordionDetails>
          </CustomAccordion>
        ))}
      </AccordionDetails>
    </CustomAccordion>
  )
}
