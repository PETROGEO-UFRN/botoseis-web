/// <reference types="vite/client" />

import createCache from '@emotion/cache'
import { CacheProvider } from '@emotion/react'
import fontsourceVariableRobotoCss from '@fontsource-variable/roboto?url'
import { CssBaseline, ThemeProvider } from '@mui/material'
import {
  createRootRoute,
  HeadContent,
  Outlet,
  Scripts
} from '@tanstack/react-router'
import { TanStackRouterDevtools } from '@tanstack/react-router-devtools'

import type { ReactNode } from 'react'

import { theme } from '@/styles/theme'

interface IWrapperComponentProps {
  children: ReactNode
}

export const Route = createRootRoute({
  head: () => ({
    links: [{ rel: 'stylesheet', href: fontsourceVariableRobotoCss }]
  }),
  component: RootComponent
})

function RootComponent() {
  return (
    <RootDocument>
      <Outlet />
    </RootDocument>
  )
}

function Providers({ children }: IWrapperComponentProps) {
  const emotionCache = createCache({ key: 'css' })

  return (
    <CacheProvider value={emotionCache}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </ThemeProvider>
    </CacheProvider>
  )
}

function RootDocument({ children }: IWrapperComponentProps) {
  return (
    <html lang="en">
      <head>
        <HeadContent />
      </head>

      <body>
        <Providers>{children}</Providers>

        <TanStackRouterDevtools position="bottom-right" />
        <Scripts />
      </body>
    </html>
  )
}
