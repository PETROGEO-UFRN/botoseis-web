import { useState, useEffect } from "react"
import type { FormEvent } from "react"
import { useNavigate } from "@tanstack/react-location"

import TextField from "@mui/material/TextField"
import Button from "@mui/material/Button"

import { validateSession, createNewSession } from "services/sessionServices";
import {
  Container,
  LoginForm,
  LinksBox,
  Link
} from "./styles"


export default function Login() {
  const navigate = useNavigate()

  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const submitLogin = (event: FormEvent) => {
    event.preventDefault()
    setIsLoading(true)

    createNewSession({ email, password }).then(response => {
      if (!response) return
      navigate({ to: "/projects" })
    })

    setIsLoading(false)
  }

  useEffect(() => {
    validateSession().then((isValid) => {
      if (isValid)
        return navigate({ to: "/projects" })
      localStorage.removeItem("jwt")
    })
  }, [])

  return (
    <Container>
      <LoginForm onSubmit={submitLogin}>
        <TextField
          type="email"
          label="E-mail"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
        />
        <TextField
          type="password"
          label="Password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
        />

        <Button
          type="submit"
          variant="contained"
          loading={isLoading}
        >
          Login
        </Button>

        <LinksBox>
          <Link to="/account-recovery">
            Esqueci minha senha
          </Link>
          <Link to="/request-access">
            Solicitar acesso
          </Link>
        </LinksBox>
      </LoginForm>
    </Container>
  )
}
