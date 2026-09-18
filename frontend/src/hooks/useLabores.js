import { useCallback, useEffect, useState } from 'react'
import { laboresApi } from '@/services/api'

export function useLabores(params = {}) {
  const [labores, setLabores] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchLabores = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await laboresApi.list(params)
      setLabores(data.items ?? data)
    } catch (err) {
      setError(err)
    } finally {
      setLoading(false)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [JSON.stringify(params)])

  useEffect(() => {
    fetchLabores()
  }, [fetchLabores])

  return { labores, loading, error, refetch: fetchLabores }
}
