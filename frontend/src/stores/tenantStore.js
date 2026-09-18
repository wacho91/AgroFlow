import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export const useTenantStore = create(
  persist(
    (set) => ({
      tenant: null,
      setTenant: (tenant) => {
        if (tenant?.id) localStorage.setItem('agroflow_tenant_id', tenant.id)
        set({ tenant })
      },
      clearTenant: () => {
        localStorage.removeItem('agroflow_tenant_id')
        set({ tenant: null })
      },
    }),
    { name: 'agroflow-tenant' },
  ),
)
