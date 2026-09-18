import { useCallback, useEffect, useState } from 'react'
import { insumosApi } from '@/services/api'

export function useInsumos(params = {}) {
  const [insumos, setInsumos] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchInsumos = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await insumosApi.list(params)
      setInsumos(data.items ?? data)
    } catch (err) {
      setError(err)
    } finally {
      setLoading(false)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [JSON.stringify(params)])

  useEffect(() => {
    fetchInsumos()
  }, [fetchInsumos])

  return { insumos, loading, error, refetch: fetchInsumos }
}
