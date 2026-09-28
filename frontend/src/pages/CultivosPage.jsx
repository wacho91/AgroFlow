import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Swal from 'sweetalert2';

export default function CultivosPage() {
  const navigate = useNavigate();
  const [cultivos, setCultivos] = useState([]);
  const [form, setForm] = useState({ nombre: '', codigo: '', variedad: '', ciclo_dias: 90, unidad_medida: 'kg' });
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const token = localStorage.getItem('agroflow_token');

  const fetchCultivos = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/v1/cultivos/', { headers: { 'Authorization': `Bearer ${token}` } });
      const data = await res.json();
      setCultivos(data);
    } catch (err) {
      Swal.fire('Error', 'No se pudieron cargar los cultivos', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { if (!token) { navigate('/login'); return; } fetchCultivos(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    const method = editingId ? 'PUT' : 'POST';
    const url = editingId ? `http://localhost:8000/api/v1/cultivos/${editingId}` : 'http://localhost:8000/api/v1/cultivos/';
    
    try {
      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify(form)
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Ocurrió un error');
      
      Swal.fire({ icon: 'success', title: editingId ? '¡Actualizado!' : '¡Creado!', confirmButtonColor: '#65a30d', timer: 1500, timerProgressBar: true });
      
      setForm({ nombre: '', codigo: '', variedad: '', ciclo_dias: 90, unidad_medida: 'kg' });
      setEditingId(null);
      fetchCultivos();
    } catch (err) {
      Swal.fire('Error', err.message, 'error');
    } finally {
      setSaving(false);
    }
  };

  const handleEdit = (cultivo) => {
    setForm(cultivo);
    setEditingId(cultivo.id);
  };

  const handleCancelEdit = () => {
    setForm({ nombre: '', codigo: '', variedad: '', ciclo_dias: 90, unidad_medida: 'kg' });
    setEditingId(null);
  };

  const handleDelete = (id) => {
    Swal.fire({
      title: '¿Eliminar cultivo?',
      text: "Esta acción no se puede revertir.",
      icon: 'warning', showCancelButton: true,
      confirmButtonColor: '#d33', cancelButtonColor: '#64748b',
      confirmButtonText: 'Sí, eliminar'
    }).then(async (result) => {
      if (result.isConfirmed) {
        try {
          await fetch(`http://localhost:8000/api/v1/cultivos/${id}`, { method: 'DELETE', headers: { 'Authorization': `Bearer ${token}` } });
          Swal.fire('¡Eliminado!', 'El cultivo fue eliminado.', 'success');
          fetchCultivos();
        } catch (err) { Swal.fire('Error', 'No se pudo eliminar.', 'error'); }
      }
    });
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-lime-700">Gestión de Cultivos 🌿</h1>
        <p className="text-slate-500">Define las especies que vas a sembrar en tus lotes.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="md:col-span-1">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
            <h2 className="text-xl font-semibold text-slate-800 mb-4">{editingId ? 'Editar Cultivo' : 'Nuevo Cultivo'}</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Nombre</label>
                <input type="text" required value={form.nombre} onChange={(e) => setForm({...form, nombre: e.target.value})} className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-lime-500" placeholder="Café Arabigo" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Código</label>
                <input type="text" required value={form.codigo} onChange={(e) => setForm({...form, codigo: e.target.value})} className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-lime-500" placeholder="CAFE-001" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Variedad (Opcional)</label>
                <input type="text" value={form.variedad} onChange={(e) => setForm({...form, variedad: e.target.value})} className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-lime-500" placeholder="Bourbon" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Ciclo (Días)</label>
                <input type="number" required value={form.ciclo_dias} onChange={(e) => setForm({...form, ciclo_dias: parseInt(e.target.value)})} className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-lime-500" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Unidad de Cosecha</label>
                <select value={form.unidad_medida} onChange={(e) => setForm({...form, unidad_medida: e.target.value})} className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-lime-500 bg-white">
                  <option value="kg">Kilogramos (kg)</option>
                  <option value="ton">Toneladas (ton)</option>
                  <option value="und">Unidades (und)</option>
                </select>
              </div>
              <div className="flex gap-2">
                <button type="submit" disabled={saving} className="w-full bg-lime-600 text-white py-2 rounded-lg font-semibold hover:bg-lime-700 disabled:opacity-50">
                  {saving ? 'Guardando...' : (editingId ? '✓ Actualizar' : '+ Crear Cultivo')}
                </button>
                {editingId && <button type="button" onClick={handleCancelEdit} className="bg-slate-200 text-slate-700 px-4 py-2 rounded-lg font-semibold hover:bg-slate-300">✕</button>}
              </div>
            </form>
          </div>
        </div>

        <div className="md:col-span-2">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
            <h2 className="text-xl font-semibold text-slate-800 mb-4">Catálogo de Cultivos</h2>
            {loading ? <p className="text-slate-400">Cargando...</p> : cultivos.length === 0 ? <p className="text-slate-400 italic">No hay cultivos registrados.</p> : (
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-slate-50 border-b border-slate-200">
                    <tr>
                      <th className="px-4 py-3 font-semibold text-slate-600">Código</th>
                      <th className="px-4 py-3 font-semibold text-slate-600">Nombre</th>
                      <th className="px-4 py-3 font-semibold text-slate-600">Variedad</th>
                      <th className="px-4 py-3 font-semibold text-slate-600">Ciclo (días)</th>
                      <th className="px-4 py-3 font-semibold text-slate-600 text-right">Acciones</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {cultivos.map((cultivo) => (
                      <tr key={cultivo.id} className="hover:bg-slate-50">
                        <td className="px-4 py-3 font-medium text-slate-800">{cultivo.codigo}</td>
                        <td className="px-4 py-3 text-slate-600">{cultivo.nombre}</td>
                        <td className="px-4 py-3 text-slate-500">{cultivo.variedad || '—'}</td>
                        <td className="px-4 py-3 text-slate-500">{cultivo.ciclo_dias}</td>
                        <td className="px-4 py-3 text-right whitespace-nowrap">
                          <button onClick={() => handleEdit(cultivo)} className="text-sky-600 hover:text-sky-800 font-medium mr-3">Editar</button>
                          <button onClick={() => handleDelete(cultivo.id)} className="text-red-500 hover:text-red-700 font-medium">Eliminar</button>
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