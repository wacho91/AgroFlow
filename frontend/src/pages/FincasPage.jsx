import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export default function FincasPage() {
  const navigate = useNavigate();
  const [fincas, setFincas] = useState([]);
  const [form, setForm] = useState({ nombre: '', codigo: '', area_total_ha: 1, municipio: '', departamento: '' });
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const token = localStorage.getItem('agroflow_token');

  const fetchFincas = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/v1/fincas/', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.status === 401) { navigate('/login'); return; }
      const data = await res.json();
      setFincas(data);
    } catch (err) {
      setError('Error al cargar fincas');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!token) { navigate('/login'); return; }
    fetchFincas();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    const method = editingId ? 'PUT' : 'POST';
    const url = editingId ? `http://localhost:8000/api/v1/fincas/${editingId}` : 'http://localhost:8000/api/v1/fincas/';
    
    try {
      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify(form)
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Error al guardar la finca');
      
      setForm({ nombre: '', codigo: '', area_total_ha: 1, municipio: '', departamento: '' });
      setEditingId(null);
      fetchFincas();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleEdit = (finca) => {
    setForm(finca);
    setEditingId(finca.id);
  };

  const handleCancelEdit = () => {
    setForm({ nombre: '', codigo: '', area_total_ha: 1, municipio: '', departamento: '' });
    setEditingId(null);
  };

  const handleDelete = async (id) => {
    if (!window.confirm("¿Seguro que quieres eliminar esta finca?")) return;
    try {
      await fetch(`http://localhost:8000/api/v1/fincas/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      fetchFincas();
    } catch (err) {
      setError("Error al eliminar");
    }
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-emerald-700">Gestión de Fincas 🌱</h1>
        <p className="text-slate-500">Registra y administra tus predios agrícolas.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="md:col-span-1">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
            <h2 className="text-xl font-semibold text-slate-800 mb-4">{editingId ? 'Editar Finca' : 'Nueva Finca'}</h2>
            {error && <div className="bg-red-50 text-red-600 p-2 rounded mb-4 text-sm">{error}</div>}
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Nombre</label>
                <input type="text" required value={form.nombre} onChange={(e) => setForm({...form, nombre: e.target.value})} className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500" placeholder="Finca La Esperanza" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Código</label>
                <input type="text" required value={form.codigo} onChange={(e) => setForm({...form, codigo: e.target.value})} className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500" placeholder="FL-001" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Área Total (Hectáreas)</label>
                <input type="number" required step="0.1" value={form.area_total_ha} onChange={(e) => setForm({...form, area_total_ha: parseFloat(e.target.value)})} className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Municipio</label>
                <input type="text" value={form.municipio} onChange={(e) => setForm({...form, municipio: e.target.value})} className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500" placeholder="Pereira" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Departamento</label>
                <input type="text" value={form.departamento} onChange={(e) => setForm({...form, departamento: e.target.value})} className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500" placeholder="Risaralda" />
              </div>
              <div className="flex gap-2">
                <button type="submit" className="w-full bg-emerald-600 text-white py-2 rounded-lg font-semibold hover:bg-emerald-700">
                  {editingId ? '✓ Actualizar' : '+ Crear Finca'}
                </button>
                {editingId && (
                  <button type="button" onClick={handleCancelEdit} className="bg-slate-200 text-slate-700 px-4 py-2 rounded-lg font-semibold hover:bg-slate-300">
                    ✕
                  </button>
                )}
              </div>
            </form>
          </div>
        </div>

        <div className="md:col-span-2">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
            <h2 className="text-xl font-semibold text-slate-800 mb-4">Fincas Registradas</h2>
            {loading ? <p className="text-slate-400">Cargando...</p> : fincas.length === 0 ? <p className="text-slate-400 italic">Aún no hay fincas registradas.</p> : (
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-slate-50 border-b border-slate-200">
                    <tr>
                      <th className="px-4 py-3 font-semibold text-slate-600">Nombre</th>
                      <th className="px-4 py-3 font-semibold text-slate-600">Código</th>
                      <th className="px-4 py-3 font-semibold text-slate-600">Área</th>
                      <th className="px-4 py-3 font-semibold text-slate-600">Ubicación</th>
                      <th className="px-4 py-3 font-semibold text-slate-600 text-right">Acciones</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {fincas.map((finca) => (
                      <tr key={finca.id} className="hover:bg-slate-50">
                        <td className="px-4 py-3 font-medium text-slate-800">{finca.nombre}</td>
                        <td className="px-4 py-3 text-slate-500">{finca.codigo}</td>
                        {/* === UNIDAD DE MEDIDA AGREGADA === */}
                        <td className="px-4 py-3 text-slate-500">{finca.area_total_ha} <span className="text-xs text-slate-400">ha</span></td>
                        <td className="px-4 py-3 text-slate-500">{finca.municipio || '—'}, {finca.departamento || '—'}</td>
                        <td className="px-4 py-3 text-right whitespace-nowrap">
                          <button onClick={() => handleEdit(finca)} className="text-sky-600 hover:text-sky-800 font-medium mr-3">Editar</button>
                          <button onClick={() => handleDelete(finca.id)} className="text-red-500 hover:text-red-700 font-medium">Eliminar</button>
                        </td>
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
  );
}