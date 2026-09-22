import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export default function FincasPage() {
  const navigate = useNavigate();
  const [fincas, setFincas] = useState([]);
  const [form, setForm] = useState({ nombre: '', codigo: '', area_total_ha: 1, municipio: '', departamento: '' });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Obtenemos el token de sesión
  const token = localStorage.getItem('agroflow_token');

  // Función para traer las fincas del backend
  const fetchFincas = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/v1/fincas/', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.status === 401) {
        navigate('/login'); // Si el token no sirve, al login
        return;
      }
      const data = await res.json();
      setFincas(data);
    } catch (err) {
      setError('Error al cargar fincas');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!token) {
      navigate('/login');
      return;
    }
    fetchFincas();
  }, []);

  // Función para crear una finca nueva
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const res = await fetch('http://localhost:8000/api/v1/fincas/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(form)
      });
      
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Error al crear la finca');
      
      setForm({ nombre: '', codigo: '', area_total_ha: 1, municipio: '', departamento: '' });
      fetchFincas(); // Refrescamos la lista
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="bg-slate-50 p-8">
      <div className="max-w-6xl mx-auto">
        
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-emerald-700">Gestión de Fincas 🌱</h1>
            <p className="text-slate-500">Registra y administra tus predios agrícolas.</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          
          {/* Formulario de Registro */}
          <div className="md:col-span-1">
            <div className="bg-white p-6 rounded-xl shadow-md border border-slate-200">
              <h2 className="text-xl font-semibold text-slate-800 mb-4">Nueva Finca</h2>
              {error && <div className="bg-red-50 text-red-600 p-2 rounded mb-4 text-sm">{error}</div>}
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-600 mb-1">Nombre</label>
                  <input 
                    type="text" required
                    value={form.nombre}
                    onChange={(e) => setForm({...form, nombre: e.target.value})}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                    placeholder="Finca La Esperanza"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-600 mb-1">Código</label>
                  <input 
                    type="text" required
                    value={form.codigo}
                    onChange={(e) => setForm({...form, codigo: e.target.value})}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                    placeholder="FL-001"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-600 mb-1">Área Total (Hectáreas)</label>
                  <input 
                    type="number" required step="0.1"
                    value={form.area_total_ha}
                    onChange={(e) => setForm({...form, area_total_ha: parseFloat(e.target.value)})}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-600 mb-1">Municipio</label>
                  <input 
                    type="text"
                    value={form.municipio}
                    onChange={(e) => setForm({...form, municipio: e.target.value})}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                    placeholder="Pereira"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-600 mb-1">Departamento</label>
                  <input 
                    type="text"
                    value={form.departamento}
                    onChange={(e) => setForm({...form, departamento: e.target.value})}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                    placeholder="Risaralda"
                  />
                </div>
                <button type="submit" className="w-full bg-emerald-600 text-white py-2 rounded-lg font-semibold hover:bg-emerald-700">
                  + Crear Finca
                </button>
              </form>
            </div>
          </div>

          {/* Lista de Fincas */}
          <div className="md:col-span-2">
            <div className="bg-white p-6 rounded-xl shadow-md border border-slate-200">
              <h2 className="text-xl font-semibold text-slate-800 mb-4">Fincas Registradas</h2>
              {loading ? (
                <p className="text-slate-400">Cargando...</p>
              ) : fincas.length === 0 ? (
                <p className="text-slate-400 italic">Aún no hay fincas registradas. Crea la primera.</p>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-sm">
                    <thead className="bg-slate-50 border-b border-slate-200">
                      <tr>
                        <th className="px-4 py-3 font-semibold text-slate-600">Nombre</th>
                        <th className="px-4 py-3 font-semibold text-slate-600">Código</th>
                        <th className="px-4 py-3 font-semibold text-slate-600">Área (ha)</th>
                        <th className="px-4 py-3 font-semibold text-slate-600">Ubicación</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {fincas.map((finca) => (
                        <tr key={finca.id} className="hover:bg-slate-50">
                          <td className="px-4 py-3 font-medium text-slate-800">{finca.nombre}</td>
                          <td className="px-4 py-3 text-slate-500">{finca.codigo}</td>
                          <td className="px-4 py-3 text-slate-500">{finca.area_total_ha}</td>
                          <td className="px-4 py-3 text-slate-500">{finca.municipio || '—'}, {finca.departamento || '—'}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}