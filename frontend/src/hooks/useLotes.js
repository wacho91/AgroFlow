import { useCallback, useEffect, useState } from 'react'
import { lotesApi } from '@/services/api'

export function useLotes(params = {}) {
  const [lotes, setLotes] = useState([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchLotes = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await lotesApi.list(params)
      setLotes(data.items ?? data)
      setTotal(data.total ?? (data.items?.length ?? 0))
    } catch (err) {
      setError(err)
    } finally {
      setLoading(false)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [JSON.stringify(params)])

  useEffect(() => {
    fetchLotes()
  }, [fetchLotes])

  const createLote = async (payload) => {
    const created = await lotesApi.create(payload)
    setLotes((prev) => [created, ...prev])
    return created
  }

  const updateLote = async (id, payload) => {
    const updated = await lotesApi.update(id, payload)
    setLotes((prev) => prev.map((l) => (l.id === id ? updated : l)))
    return updated
  }

  const removeLote = async (id) => {
    await lotesApi.remove(id)
    setLotes((prev) => prev.filter((l) => l.id !== id))
  }

  return {
    lotes,
    total,
    loading,
    error,
    refetch: fetchLotes,
    createLote,
    updateLote,
    removeLote,
  }
}
