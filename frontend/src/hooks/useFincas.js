import { useCallback, useEffect, useState } from 'react'
import { fincasApi } from '@/services/api'

export function useFincas(params = {}) {
  const [fincas, setFincas] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchFincas = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await fincasApi.list(params)
      setFincas(data.items ?? data)
    } catch (err) {
      setError(err)
    } finally {
      setLoading(false)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [JSON.stringify(params)])

  useEffect(() => {
    fetchFincas()
  }, [fetchFincas])

  return { fincas, loading, error, refetch: fetchFincas }
}
