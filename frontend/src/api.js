const API_URL = `${(import.meta.env.VITE_API_URL || '').replace(/\/$/, '')}/api/libros`

async function request(url = '', options = {}) {
  const response = await fetch(`${API_URL}${url}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  })

  if (!response.ok) {
    let details
    try {
      details = await response.json()
    } catch {
      details = null
    }
    const error = new Error('La solicitud no pudo completarse.')
    error.status = response.status
    error.details = details
    throw error
  }

  return response.status === 204 ? null : response.json()
}

export const librosApi = {
  listar: () => request(),
  crear: (libro) => request('', { method: 'POST', body: JSON.stringify(libro) }),
  eliminar: (id) => request(`/${id}`, { method: 'DELETE' }),
}

