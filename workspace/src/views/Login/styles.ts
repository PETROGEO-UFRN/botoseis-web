import styled from 'styled-components'
import { Link as TanstackLink } from "@tanstack/react-location"

export const Container = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;

  width: 100vw;
  height: 100vh;
  background-color: ${({ theme }) => theme.palette.primary.light};
`

export const LoginForm = styled.form`
  display: flex;
  flex-direction: column;
  background-color: ${({ theme }) => theme.palette.background.default};
  width: 92%;
  max-width: 512px;

  border-radius: 4px;
  padding: 32px 16px;
  gap: 8px;
`

export const LinksBox = styled.div`
  display: flex;
  flex-direction: column;
  margin-top: 32px;
  gap: 8px;
`

export const Link = styled(TanstackLink)`
  font-size: 14px;
`
