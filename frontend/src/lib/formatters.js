export const formatCurrency = (value, currency = 'COP') => {
  const num = Number(value ?? 0)
  return new Intl.NumberFormat('es-CO', {
    style: 'currency',
    currency,
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
  }).format(num)
}

export const formatNumber = (value, decimals = 2) => {
  const num = Number(value ?? 0)
  return new Intl.NumberFormat('es-CO', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(num)
}

export const formatDate = (value) => {
  if (!value) return '—'
  const date = new Date(value)
  return new Intl.DateTimeFormat('es-CO', {
    year: 'numeric',
    month: 'short',
    day: '2-digit',
  }).format(date)
}

export const formatDateTime = (value) => {
  if (!value) return '—'
  const date = new Date(value)
  return new Intl.DateTimeFormat('es-CO', {
    year: 'numeric',
    month: 'short',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date)
}

export const formatPercent = (value, decimals = 1) => {
  const num = Number(value ?? 0)
  return `${num.toFixed(decimals)}%`
}
