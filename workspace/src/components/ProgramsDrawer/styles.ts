import styled from "styled-components"
import Typography from "@mui/material/Typography"
import Accordion from '@mui/material/Accordion'
import ListItem from '@mui/material/ListItem'
import IconButton from '@mui/material/IconButton'
import AccordionSummary from '@mui/material/AccordionSummary';

export const Container = styled.div`
  overflow: hidden;
  height: 100%;
  display: flex;
  flex-direction: column;
`

export const GroupsListBox = styled.div`
  overflow-y: auto;
  height: 100%;
`

export const PackageAccordionSummary = styled(AccordionSummary)`
  && > .MuiAccordionSummary-content {
    justify-content: center;
    align-items: center;
  }
`

export const Title = styled(Typography)`
  && {
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 1.2px;
  }
`

export const CloseButton = styled(IconButton)`
  position: absolute !important;
  z-index: 10;
`

export const CustomAccordion = styled(Accordion)`
  && {
    box-shadow: none;
  }
`

export const CustomListItem = styled(ListItem)`
  &:not(:last-child) {
    border-bottom: 1px solid ${({ theme }) => theme.palette.divider};
  }
  svg:not(:first-child) {
    opacity: 0.37;
  }
`