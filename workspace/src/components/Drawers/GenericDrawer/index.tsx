import { Dispatch, ReactNode, SetStateAction, useMemo } from 'react'
import Drawer from "@mui/material/Drawer"

interface IGenericDrawerProps {
  isOpen: boolean
  setIsOpen: Dispatch<SetStateAction<boolean>>
  anchor: 'right' | 'bottom'
  children: ReactNode
}

export default function GenericDrawer({
  isOpen,
  setIsOpen,
  anchor,
  children
}: IGenericDrawerProps) {
  const drawerWidth = useMemo(() => {
    if (anchor === "right")
      return 448
    return 'auto'
  }, [anchor])

  return (
    <Drawer
      open={isOpen}
      anchor={anchor}
      onClose={() => setIsOpen(false)}
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
          gap: "0",
          padding: "8px",
          zIndex: 100,
        },
      }}
      variant="persistent"
    >
      {children}
    </Drawer>
  )
}
