import { useCallback, useEffect, useState } from 'react'
import { costosApi } from '@/services/api'

export function useCostos(params = {}) {
  const [costos, setCostos] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchCostos = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await costosApi.list(params)
      setCostos(data.items ?? data)
    } catch (err) {
      setError(err)
    } finally {
      setLoading(false)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [JSON.stringify(params)])

  useEffect(() => {
    fetchCostos()
  }, [fetchCostos])

  const createCosto = async (payload) => {
    const created = await costosApi.create(payload)
    setCostos((prev) => [created, ...prev])
    return created
  }

  return { costos, loading, error, refetch: fetchCostos, createCosto }
}
