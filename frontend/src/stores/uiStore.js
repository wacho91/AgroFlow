import { create } from 'zustand'

export const useUiStore = create((set) => ({
  sidebarCollapsed: false,
  toggleSidebar: () => set((s) => ({ sidebarCollapsed: !s.sidebarCollapsed })),
  toasts: [],
  pushToast: (toast) =>
    set((s) => ({
      toasts: [
        ...s.toasts,
        { id: Date.now() + Math.random(), ...toast },
      ],
    })),
  removeToast: (id) =>
    set((s) => ({ toasts: s.toasts.filter((t) => t.id !== id) })),
}))
