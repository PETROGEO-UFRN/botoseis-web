import type { Dispatch, SetStateAction } from 'react'
import { format } from 'date-fns'
import { useShallow } from 'zustand/react/shallow'

import Table from '@mui/material/Table'
import TableBody from '@mui/material/TableBody'
import TableHead from '@mui/material/TableHead'
import TableRow from '@mui/material/TableRow'
import AccessTimeRoundedIcon from '@mui/icons-material/AccessTimeRounded'

import { CloseButton } from 'shared-ui'

import { useLogsStore } from 'store/logsStore'
import { useSelectedWorkflowsStore } from 'store/selectedWorkflowsStore'
import GenericDrawer from '../GenericDrawer'

import {
  CustomTableContainer,
  CustomTableCell,
  IconCellContainer,
} from './styles'

interface IConsoleProps {
  isOpen: boolean
  setIsOpen: Dispatch<SetStateAction<boolean>>
}

function getFormatedDate(dateString: string): string {
  const date = new Date(dateString)
  return `${format(date, 'HH:mm:ss')}`
}

export default function Console({ isOpen, setIsOpen }: IConsoleProps) {
  const consoleLogs = useLogsStore(useShallow((state) => state.logs))
  const selectedWorkflowId = useSelectedWorkflowsStore(useShallow((state) => (
    state.singleSelectedWorkflowId
  )))

  return (
    <GenericDrawer
      isOpen={isOpen}
      setIsOpen={setIsOpen}
      anchor='bottom'
    >
      <CloseButton
        onClick={() => setIsOpen(false)}
        $top={"2px"}
      />
      <CustomTableContainer>
        <Table
          size="small"
          stickyHeader
          padding='none'
        >
          <TableHead>
            <TableRow>
              <CustomTableCell variant="head">
                Command
              </CustomTableCell>
              <CustomTableCell variant="head">
                Message
              </CustomTableCell>
              <CustomTableCell
                variant="head"
                $isShort
                $hasDivider
              >
                Starting at
              </CustomTableCell>
              <CustomTableCell
                variant="head"
                $isShort
              >
                Endindg at
              </CustomTableCell>
            </TableRow>
          </TableHead>

          <TableBody>
            {selectedWorkflowId && consoleLogs.get(selectedWorkflowId)?.map((log) => (
              <TableRow key={log.processStartTime} hover>
                <CustomTableCell>
                  {log.executionSimplifiedString}
                </CustomTableCell>
                <CustomTableCell>
                  {log.logMessage.split('\n').map((line, index) => (
                    <p key={index}>{line}</p>
                  ))}
                </CustomTableCell>

                <CustomTableCell
                  $isShort
                  $hasDivider
                >
                  <IconCellContainer>
                    <AccessTimeRoundedIcon fontSize='small' />
                    {getFormatedDate(log.processStartTime)}
                  </IconCellContainer>
                </CustomTableCell>
                <CustomTableCell $isShort>
                  <IconCellContainer>
                    <AccessTimeRoundedIcon fontSize='small' />
                    {getFormatedDate(log.executionEndTime)}
                  </IconCellContainer>
                </CustomTableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CustomTableContainer>
    </GenericDrawer>
  )
}
