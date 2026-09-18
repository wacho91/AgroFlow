import { useCallback, useEffect, useState } from 'react'
import { jornalerosApi } from '@/services/api'

export function useJornaleros(params = {}) {
  const [jornaleros, setJornaleros] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchJornaleros = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await jornalerosApi.list(params)
      setJornaleros(data.items ?? data)
    } catch (err) {
      setError(err)
    } finally {
      setLoading(false)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [JSON.stringify(params)])

  useEffect(() => {
    fetchJornaleros()
  }, [fetchJornaleros])

  return { jornaleros, loading, error, refetch: fetchJornaleros }
}
