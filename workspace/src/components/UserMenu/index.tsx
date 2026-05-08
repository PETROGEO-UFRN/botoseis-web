import { useState } from 'react';
import { useNavigate } from '@tanstack/react-location';

import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import IconButton from '@mui/material/IconButton';

import PersonRoundedIcon from '@mui/icons-material/PersonRounded'

export default function UserMenu() {
  const navigate = useNavigate()
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);

  const handleClose = () => {
    setAnchorEl(null);
  };

  const logout = () => {
    navigate({ to: "/login" })
    handleClose()
  }

  return (
    <>
      <IconButton
        onClick={(event) => setAnchorEl(event.currentTarget)}
      >
        <PersonRoundedIcon htmlColor='#fff' />
      </IconButton>
      <Menu
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
      >
        <MenuItem onClick={logout}>
          Logout
        </MenuItem>
      </Menu>
    </>
  )
}
