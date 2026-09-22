import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export default function LotesPage() {
  const navigate = useNavigate();
  const [lotes, setLotes] = useState([]);
  const [fincas, setFincas] = useState([]);
  const [form, setForm] = useState({ finca_id: '', nombre: '', codigo: '', area_ha: 1, estado: 'disponible' });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const token = localStorage.getItem('agroflow_token');

  const fetchLotes = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/v1/lotes/', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await res.json();
      setLotes(data);
    } catch (err) {
      setError('Error al cargar lotes');
    }
  };

  const fetchFincas = async () => {
    const res = await fetch('http://localhost:8000/api/v1/fincas/', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await res.json();
    setFincas(data);
    if (data.length > 0) {
      setForm(prev => ({ ...prev, finca_id: data[0].id })); // Selecciona la primera finca por defecto
    }
  };

  useEffect(() => {
    if (!token) {
      navigate('/login');
      return;
    }
    Promise.all([fetchFincas(), fetchLotes()]).finally(() => setLoading(false));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    if (!form.finca_id) {
      setError("Debes crear una finca primero antes de registrar lotes.");
      return;
    }
    try {
      const res = await fetch('http://localhost:8000/api/v1/lotes/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(form)
      });
      
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Error al crear el lote');
      
      setForm(prev => ({ ...prev, nombre: '', codigo: '', area_ha: 1 }));
      fetchLotes();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="bg-slate-50 p-8">
      <div className="max-w-6xl mx-auto">
        
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-amber-600">Gestión de Lotes 🗺️</h1>
            <p className="text-slate-500">Divide tu finca en parcelas para sembrar.</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          
          {/* Formulario de Registro */}
          <div className="md:col-span-1">
            <div className="bg-white p-6 rounded-xl shadow-md border border-slate-200">
              <h2 className="text-xl font-semibold text-slate-800 mb-4">Nuevo Lote</h2>
              {error && <div className="bg-red-50 text-red-600 p-2 rounded mb-4 text-sm">{error}</div>}
              <form onSubmit={handleSubmit} className="space-y-4">
                
                <div>
                  <label className="block text-sm font-medium text-slate-600 mb-1">Finca (Predio)</label>
                  <select 
                    value={form.finca_id}
                    onChange={(e) => setForm({...form, finca_id: e.target.value})}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-amber-500 bg-white"
                    required
                  >
                    {fincas.map(f => <option key={f.id} value={f.id}>{f.nombre}</option>)}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-600 mb-1">Nombre del Lote</label>
                  <input 
                    type="text" required
                    value={form.nombre}
                    onChange={(e) => setForm({...form, nombre: e.target.value})}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-amber-500"
                    placeholder="Lote Norte 1"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-600 mb-1">Código</label>
                  <input 
                    type="text" required
                    value={form.codigo}
                    onChange={(e) => setForm({...form, codigo: e.target.value})}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-amber-500"
                    placeholder="LT-001"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-600 mb-1">Área (Hectáreas)</label>
                  <input 
                    type="number" required step="0.1"
                    value={form.area_ha}
                    onChange={(e) => setForm({...form, area_ha: parseFloat(e.target.value)})}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-amber-500"
                  />
                </div>
                <button type="submit" className="w-full bg-amber-600 text-white py-2 rounded-lg font-semibold hover:bg-amber-700">
                  + Crear Lote
                </button>
              </form>
            </div>
          </div>

          {/* Lista de Lotes */}
          <div className="md:col-span-2">
            <div className="bg-white p-6 rounded-xl shadow-md border border-slate-200">
              <h2 className="text-xl font-semibold text-slate-800 mb-4">Lotes Registrados</h2>
              {loading ? (
                <p className="text-slate-400">Cargando...</p>
              ) : lotes.length === 0 ? (
                <p className="text-slate-400 italic">Aún no hay lotes registrados.</p>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-sm">
                    <thead className="bg-slate-50 border-b border-slate-200">
                      <tr>
                        <th className="px-4 py-3 font-semibold text-slate-600">Código</th>
                        <th className="px-4 py-3 font-semibold text-slate-600">Nombre</th>
                        <th className="px-4 py-3 font-semibold text-slate-600">Área (ha)</th>
                        <th className="px-4 py-3 font-semibold text-slate-600">Estado</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {lotes.map((lote) => {
                        const finca = fincas.find(f => f.id === lote.finca_id);
                        return (
                          <tr key={lote.id} className="hover:bg-slate-50">
                            <td className="px-4 py-3 font-medium text-slate-800">{lote.codigo}</td>
                            <td className="px-4 py-3 text-slate-500">
                              {Number(lote.area_ha) % 1 === 0 ? Number(lote.area_ha) : Number(lote.area_ha).toFixed(2)} <span className="text-xs text-slate-400">ha</span>
                            </td>
                            <td className="px-4 py-3 text-slate-500">{lote.area_ha}</td>
                            <td className="px-4 py-3">
                              <span className="bg-green-100 text-green-700 px-2 py-1 rounded-full text-xs font-medium">
                                {lote.estado}
                              </span>
                            </td>
                          </tr>
                        );
                      })}
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