import { useCallback, useEffect, useState } from 'react'
import { ciclosApi } from '@/services/api'

export function useCiclos(params = {}) {
  const [ciclos, setCiclos] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchCiclos = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await ciclosApi.list(params)
      setCiclos(data.items ?? data)
    } catch (err) {
      setError(err)
    } finally {
      setLoading(false)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [JSON.stringify(params)])

  useEffect(() => {
    fetchCiclos()
  }, [fetchCiclos])

  return { ciclos, loading, error, refetch: fetchCiclos }
}
