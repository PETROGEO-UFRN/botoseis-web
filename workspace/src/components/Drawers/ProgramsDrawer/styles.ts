import styled from "styled-components"
import Typography from "@mui/material/Typography"
import Accordion from '@mui/material/Accordion'
import AccordionSummary from '@mui/material/AccordionSummary'
import ListItem from '@mui/material/ListItem'
import IconButton from '@mui/material/IconButton'

export const Container = styled.div`
  overflow: hidden;
  height: 100%;
  display: flex;
  flex-direction: column;
`

export const CustomAccordion = styled(Accordion)`
  && {
    max-height: calc( 100% - (56.01px + 16px));
    overflow-y: auto;
    box-shadow: none;
  }
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

export const CustomListItem = styled(ListItem)`
  &:not(:last-child) {
    border-bottom: 1px solid ${({ theme }) => theme.palette.divider};
  }
  svg:not(:first-child) {
    opacity: 0.37;
  }
`

export const CloseButton = styled(IconButton)`
  position: absolute !important;
  z-index: 10;
`