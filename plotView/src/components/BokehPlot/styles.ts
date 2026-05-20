import { styled } from '@mui/material'

export const Container = styled('div')({
  position: 'relative',
  minHeight: '500px',
  display: 'flex',
  flexDirection: 'column',
  height: '100%'
})

export const PlotBox = styled('div')({
  flexGrow: 1,
  width: '100%',
  '& > div': {
    width: '100%',
    height: '100%'
  },
  '& .bk-root': {
    width: '100%',
    height: '100%',
    display: 'flex',
    justifyContent: 'center'
  },
  '& .bk-Figure': {
    width: '100%',
    height: '100%'
  },
  '& .bk-Row': {
    width: '100%',
    height: '100%'
  }
})
