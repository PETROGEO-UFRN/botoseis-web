import { useState } from 'react'
import Button from '@mui/material/Button'
import Stack from '@mui/material/Stack'
import TextField from '@mui/material/TextField'
import { IconButton, InputAdornment } from '@mui/material'
import { Visibility, VisibilityOff } from '@mui/icons-material'

export default function LoginForm() {
  const [userEmail, setUserEmail] = useState("")
  const [password, setPassword] = useState("")
  const [showPassword, setShowPassword] = useState(false)

  const togglePasswordView = () => {
    setShowPassword(!showPassword)
  }

  const submit = () => {
    // Send to API
    console.log("Email:", userEmail, "Password:", password)
  }

  return (
    <Stack direction="column" alignItems="center" sx={{ padding: "250px", height: "100hv"}}>
      <TextField
        label="Email"
        value={userEmail}
        onChange={(event) => setUserEmail(event.target.value)}
        sx={{ width: '300px', height: '100px' }}
      />
      <TextField
        label="Senha"
        type={showPassword ? "text" : "password"}
        value={password}
        onChange={(event) => setPassword(event.target.value)}
        sx={{ width: '300px', height: '100px' }}
        InputProps={{
          endAdornment: (
            <InputAdornment position="end">
              <IconButton onClick={togglePasswordView} edge="end">
                {showPassword ? <VisibilityOff /> : <Visibility />}
              </IconButton>
            </InputAdornment>
          ),
        }}
      />
      <Button variant="contained" onClick={submit} sx={{ width: '300px', height: '50px' }}>
        Submeter
      </Button>
    </Stack>
  )
}
