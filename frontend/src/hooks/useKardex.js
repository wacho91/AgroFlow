import { useCallback, useEffect, useState } from 'react'
import { kardexApi } from '@/services/api'

export function useKardex(params = {}) {
  const [movimientos, setMovimientos] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchKardex = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await kardexApi.list(params)
      setMovimientos(data.items ?? data)
    } catch (err) {
      setError(err)
    } finally {
      setLoading(false)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [JSON.stringify(params)])

  useEffect(() => {
    fetchKardex()
  }, [fetchKardex])

  return { movimientos, loading, error, refetch: fetchKardex }
}
