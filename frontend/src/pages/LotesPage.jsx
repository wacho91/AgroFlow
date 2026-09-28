import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Swal from 'sweetalert2';

export default function LotesPage() {
  const navigate = useNavigate();
  const [lotes, setLotes] = useState([]);
  const [fincas, setFincas] = useState([]);
  const [form, setForm] = useState({ finca_id: '', nombre: '', codigo: '', area_ha: 1, estado: 'disponible' });
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [saving, setSaving] = useState(false);

  const token = localStorage.getItem('agroflow_token');

  const fetchLotes = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/v1/lotes/', { headers: { 'Authorization': `Bearer ${token}` } });
      const data = await res.json();
      setLotes(data);
    } catch (err) { setError('Error al cargar lotes'); }
  };

  const fetchFincas = async () => {
    const res = await fetch('http://localhost:8000/api/v1/fincas/', { headers: { 'Authorization': `Bearer ${token}` } });
    const data = await res.json();
    setFincas(data);
    if (data.length > 0 && !editingId) setForm(prev => ({ ...prev, finca_id: data[0].id }));
  };

  useEffect(() => {
    if (!token) { navigate('/login'); return; }
    Promise.all([fetchFincas(), fetchLotes()]).finally(() => setLoading(false));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    const method = editingId ? 'PUT' : 'POST';
    const url = editingId ? `http://localhost:8000/api/v1/lotes/${editingId}` : 'http://localhost:8000/api/v1/lotes/';
    try {
      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify(form)
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Error al guardar el lote');
      
      Swal.fire({ icon: 'success', title: editingId ? '¡Actualizado!' : '¡Creado!', confirmButtonColor: '#d97706', timer: 1500, timerProgressBar: true });
      setForm({ finca_id: fincas[0]?.id || '', nombre: '', codigo: '', area_ha: 1, estado: 'disponible' });
      setEditingId(null);
      fetchLotes();
    } catch (err) {
      Swal.fire('Error', err.message, 'error');
    } finally {
      setSaving(false);
    }
  };

  const handleEdit = (lote) => {
    setForm(lote);
    setEditingId(lote.id);
  };

  const handleCancelEdit = () => {
    setForm({ finca_id: fincas[0]?.id || '', nombre: '', codigo: '', area_ha: 1, estado: 'disponible' });
    setEditingId(null);
  };

  const handleDelete = (id) => {
    Swal.fire({
      title: '¿Eliminar lote?', text: "Esta acción no se puede revertir.",
      icon: 'warning', showCancelButton: true,
      confirmButtonColor: '#d33', cancelButtonColor: '#64748b',
      confirmButtonText: 'Sí, eliminar'
    }).then(async (result) => {
      if (result.isConfirmed) {
        try {
          await fetch(`http://localhost:8000/api/v1/lotes/${id}`, { method: 'DELETE', headers: { 'Authorization': `Bearer ${token}` } });
          Swal.fire('¡Eliminado!', 'El lote fue eliminado.', 'success');
          fetchLotes();
        } catch (err) { Swal.fire('Error', 'No se pudo eliminar.', 'error'); }
      }
    });
  };

  const formatCurrency = (value) => `$${Number(value).toLocaleString('es-CO')}`;

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-amber-600">Gestión de Lotes 🗺️</h1>
        <p className="text-slate-500">Divide tu finca en parcelas para sembrar.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="md:col-span-1">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
            <h2 className="text-xl font-semibold text-slate-800 mb-4">{editingId ? 'Editar Lote' : 'Nuevo Lote'}</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Finca (Predio)</label>
                <select value={form.finca_id} onChange={(e) => setForm({...form, finca_id: e.target.value})} className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-amber-500 bg-white" required>
                  {fincas.map(f => <option key={f.id} value={f.id}>{f.nombre}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Nombre del Lote</label>
                <input type="text" required value={form.nombre} onChange={(e) => setForm({...form, nombre: e.target.value})} className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-amber-500" placeholder="Lote Norte 1" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Código</label>
                <input type="text" required value={form.codigo} onChange={(e) => setForm({...form, codigo: e.target.value})} className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-amber-500" placeholder="LT-001" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Área (Hectáreas)</label>
                <input type="number" required step="0.1" value={form.area_ha} onChange={(e) => setForm({...form, area_ha: parseFloat(e.target.value)})} className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-amber-500" />
              </div>
              <div className="flex gap-2">
                <button type="submit" disabled={saving} className="w-full bg-amber-600 text-white py-2 rounded-lg font-semibold hover:bg-amber-700 disabled:opacity-50">
                  {saving ? 'Guardando...' : (editingId ? '✓ Actualizar' : '+ Crear Lote')}
                </button>
                {editingId && <button type="button" onClick={handleCancelEdit} className="bg-slate-200 text-slate-700 px-4 py-2 rounded-lg font-semibold hover:bg-slate-300">✕</button>}
              </div>
            </form>
          </div>
        </div>

        <div className="md:col-span-2">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
            <h2 className="text-xl font-semibold text-slate-800 mb-4">Lotes Registrados</h2>
            {loading ? <p className="text-slate-400">Cargando...</p> : lotes.length === 0 ? <p className="text-slate-400 italic">Aún no hay lotes registrados.</p> : (
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-slate-50 border-b border-slate-200">
                    <tr>
                      <th className="px-4 py-3 font-semibold text-slate-600">Código</th>
                      <th className="px-4 py-3 font-semibold text-slate-600">Nombre</th>
                      <th className="px-4 py-3 font-semibold text-slate-600">Área</th>
                      <th className="px-4 py-3 font-semibold text-slate-600">Costo Acumulado</th>
                      <th className="px-4 py-3 font-semibold text-slate-600 text-right">Acciones</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {lotes.map((lote) => (
                      <tr key={lote.id} className="hover:bg-slate-50">
                        <td className="px-4 py-3 font-medium text-slate-800">{lote.codigo}</td>
                        <td className="px-4 py-3 text-slate-600">{lote.nombre}</td>
                        <td className="px-4 py-3 text-slate-500">{Number(lote.area_ha) % 1 === 0 ? Number(lote.area_ha) : Number(lote.area_ha).toFixed(2)} ha</td>
                        <td className="px-4 py-3 font-bold text-red-600">{formatCurrency(lote.costo_acumulado || 0)}</td>
                        <td className="px-4 py-3 text-right whitespace-nowrap">
                          <button onClick={() => handleEdit(lote)} className="text-sky-600 hover:text-sky-800 font-medium mr-3">Editar</button>
                          <button onClick={() => handleDelete(lote.id)} className="text-red-500 hover:text-red-700 font-medium">Eliminar</button>
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