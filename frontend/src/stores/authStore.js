import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export const useAuthStore = create(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      login: ({ user, token }) => {
        localStorage.setItem('agroflow_token', token)
        set({ user, token, isAuthenticated: true })
      },
      logout: () => {
        localStorage.removeItem('agroflow_token')
        set({ user: null, token: null, isAuthenticated: false })
      },
    }),
    { name: 'agroflow-auth' },
  ),
)
