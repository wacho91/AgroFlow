import { apiClient } from '@/lib/axios'

/**
 * Endpoints exactos del backend AgroFlow.
 * Cada método retorna la data ya desenvuelta (response.data).
 */

// ---------- Health ----------
export const healthApi = {
  check: () => apiClient.get('/health').then((r) => r.data),
}

// ---------- Tenancy ----------
export const tenantsApi = {
  list: (params) => apiClient.get('/api/v1/tenants', { params }).then((r) => r.data),
  get: (id) => apiClient.get(`/api/v1/tenants/${id}`).then((r) => r.data),
  create: (payload) => apiClient.post('/api/v1/tenants', payload).then((r) => r.data),
  update: (id, payload) => apiClient.patch(`/api/v1/tenants/${id}`, payload).then((r) => r.data),
  remove: (id) => apiClient.delete(`/api/v1/tenants/${id}`).then((r) => r.data),
}

export const usuariosApi = {
  list: (params) => apiClient.get('/api/v1/usuarios', { params }).then((r) => r.data),
  get: (id) => apiClient.get(`/api/v1/usuarios/${id}`).then((r) => r.data),
  create: (payload) => apiClient.post('/api/v1/usuarios', payload).then((r) => r.data),
  update: (id, payload) => apiClient.patch(`/api/v1/usuarios/${id}`, payload).then((r) => r.data),
  remove: (id) => apiClient.delete(`/api/v1/usuarios/${id}`).then((r) => r.data),
}

// ---------- Costos ----------
export const fincasApi = {
  list: (params) => apiClient.get('/api/v1/fincas', { params }).then((r) => r.data),
  get: (id) => apiClient.get(`/api/v1/fincas/${id}`).then((r) => r.data),
  create: (payload) => apiClient.post('/api/v1/fincas', payload).then((r) => r.data),
  update: (id, payload) => apiClient.patch(`/api/v1/fincas/${id}`, payload).then((r) => r.data),
  remove: (id) => apiClient.delete(`/api/v1/fincas/${id}`).then((r) => r.data),
}

export const lotesApi = {
  list: (params) => apiClient.get('/api/v1/lotes', { params }).then((r) => r.data),
  get: (id) => apiClient.get(`/api/v1/lotes/${id}`).then((r) => r.data),
  create: (payload) => apiClient.post('/api/v1/lotes', payload).then((r) => r.data),
  update: (id, payload) => apiClient.patch(`/api/v1/lotes/${id}`, payload).then((r) => r.data),
  remove: (id) => apiClient.delete(`/api/v1/lotes/${id}`).then((r) => r.data),
}

export const cultivosApi = {
  list: (params) => apiClient.get('/api/v1/cultivos', { params }).then((r) => r.data),
  get: (id) => apiClient.get(`/api/v1/cultivos/${id}`).then((r) => r.data),
  create: (payload) => apiClient.post('/api/v1/cultivos', payload).then((r) => r.data),
  update: (id, payload) => apiClient.patch(`/api/v1/cultivos/${id}`, payload).then((r) => r.data),
  remove: (id) => apiClient.delete(`/api/v1/cultivos/${id}`).then((r) => r.data),
}

export const ciclosApi = {
  list: (params) => apiClient.get('/api/v1/ciclos', { params }).then((r) => r.data),
  get: (id) => apiClient.get(`/api/v1/ciclos/${id}`).then((r) => r.data),
  create: (payload) => apiClient.post('/api/v1/ciclos', payload).then((r) => r.data),
  update: (id, payload) => apiClient.patch(`/api/v1/ciclos/${id}`, payload).then((r) => r.data),
  remove: (id) => apiClient.delete(`/api/v1/ciclos/${id}`).then((r) => r.data),
}

export const actividadesApi = {
  list: (params) => apiClient.get('/api/v1/actividades', { params }).then((r) => r.data),
  get: (id) => apiClient.get(`/api/v1/actividades/${id}`).then((r) => r.data),
  create: (payload) => apiClient.post('/api/v1/actividades', payload).then((r) => r.data),
  update: (id, payload) => apiClient.patch(`/api/v1/actividades/${id}`, payload).then((r) => r.data),
  remove: (id) => apiClient.delete(`/api/v1/actividades/${id}`).then((r) => r.data),
}

export const costosApi = {
  list: (params) => apiClient.get('/api/v1/costos', { params }).then((r) => r.data),
  get: (id) => apiClient.get(`/api/v1/costos/${id}`).then((r) => r.data),
  create: (payload) => apiClient.post('/api/v1/costos', payload).then((r) => r.data),
  update: (id, payload) => apiClient.patch(`/api/v1/costos/${id}`, payload).then((r) => r.data),
  remove: (id) => apiClient.delete(`/api/v1/costos/${id}`).then((r) => r.data),
}

// ---------- Inventario ----------
export const categoriasInsumoApi = {
  list: (params) => apiClient.get('/api/v1/categorias-insumo', { params }).then((r) => r.data),
  create: (payload) => apiClient.post('/api/v1/categorias-insumo', payload).then((r) => r.data),
}

export const almacenesApi = {
  list: (params) => apiClient.get('/api/v1/almacenes', { params }).then((r) => r.data),
  get: (id) => apiClient.get(`/api/v1/almacenes/${id}`).then((r) => r.data),
  create: (payload) => apiClient.post('/api/v1/almacenes', payload).then((r) => r.data),
  update: (id, payload) => apiClient.patch(`/api/v1/almacenes/${id}`, payload).then((r) => r.data),
  remove: (id) => apiClient.delete(`/api/v1/almacenes/${id}`).then((r) => r.data),
}

export const insumosApi = {
  list: (params) => apiClient.get('/api/v1/insumos', { params }).then((r) => r.data),
  get: (id) => apiClient.get(`/api/v1/insumos/${id}`).then((r) => r.data),
  create: (payload) => apiClient.post('/api/v1/insumos', payload).then((r) => r.data),
  update: (id, payload) => apiClient.patch(`/api/v1/insumos/${id}`, payload).then((r) => r.data),
  remove: (id) => apiClient.delete(`/api/v1/insumos/${id}`).then((r) => r.data),
}

export const kardexApi = {
  list: (params) => apiClient.get('/api/v1/kardex', { params }).then((r) => r.data),
  get: (id) => apiClient.get(`/api/v1/kardex/${id}`).then((r) => r.data),
  create: (payload) => apiClient.post('/api/v1/kardex', payload).then((r) => r.data),
  stock: (params) => apiClient.get('/api/v1/kardex/stock', { params }).then((r) => r.data),
}

// ---------- Nómina ----------
export const jornalerosApi = {
  list: (params) => apiClient.get('/api/v1/jornaleros', { params }).then((r) => r.data),
  get: (id) => apiClient.get(`/api/v1/jornaleros/${id}`).then((r) => r.data),
  create: (payload) => apiClient.post('/api/v1/jornaleros', payload).then((r) => r.data),
  update: (id, payload) => apiClient.patch(`/api/v1/jornaleros/${id}`, payload).then((r) => r.data),
  remove: (id) => apiClient.delete(`/api/v1/jornaleros/${id}`).then((r) => r.data),
}

export const laboresApi = {
  list: (params) => apiClient.get('/api/v1/labores', { params }).then((r) => r.data),
  get: (id) => apiClient.get(`/api/v1/labores/${id}`).then((r) => r.data),
  create: (payload) => apiClient.post('/api/v1/labores', payload).then((r) => r.data),
  update: (id, payload) => apiClient.patch(`/api/v1/labores/${id}`, payload).then((r) => r.data),
  remove: (id) => apiClient.delete(`/api/v1/labores/${id}`).then((r) => r.data),
}

export const liquidacionesApi = {
  list: (params) => apiClient.get('/api/v1/liquidaciones', { params }).then((r) => r.data),
  get: (id) => apiClient.get(`/api/v1/liquidaciones/${id}`).then((r) => r.data),
  create: (payload) => apiClient.post('/api/v1/liquidaciones', payload).then((r) => r.data),
}

export const novedadesNominaApi = {
  list: (params) => apiClient.get('/api/v1/novedades-nomina', { params }).then((r) => r.data),
  create: (payload) => apiClient.post('/api/v1/novedades-nomina', payload).then((r) => r.data),
}
