import { useEffect } from 'react'
import { useRoutes } from 'react-router-dom'
import { routes } from './router/routes'
import { useThemeStore } from './stores/themeStore'

export default function App() {
  const element = useRoutes(routes)
  const { theme } = useThemeStore()

  useEffect(() => {
    const root = document.documentElement
    if (theme === 'dark') root.classList.add('dark')
    else root.classList.remove('dark')
  }, [theme])

  return element
}
