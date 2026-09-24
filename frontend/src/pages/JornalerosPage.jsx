import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Swal from 'sweetalert2';

export default function JornalerosPage() {
  const navigate = useNavigate();
  const [jornaleros, setJornaleros] = useState([]);
  const [form, setForm] = useState({ nombre_completo: '', documento: '', telefono: '', tipo: 'temporal' });
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(true);

  const token = localStorage.getItem('agroflow_token');

  const fetchJornaleros = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/v1/jornaleros/', { headers: { 'Authorization': `Bearer ${token}` } });
      if (!res.ok) throw new Error('Error al cargar');
      const data = await res.json();
      
      // A veces el backend con paginación devuelve un objeto { items: [...] }, otras veces un array directo [...]
      const list = Array.isArray(data) ? data : (data.items || []);
      setJornaleros(list);
    } catch (err) {
      Swal.fire('Error', 'No se pudieron cargar los jornaleros', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { if (!token) { navigate('/login'); return; } fetchJornaleros(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const method = editingId ? 'PUT' : 'POST';
    // Si es PUT, usamos PATCH en la URL por cómo está hecho el router complex
    const url = editingId 
      ? `http://localhost:8000/api/v1/jornaleros/${editingId}` 
      : 'http://localhost:8000/api/v1/jornaleros/';
    
    try {
      const res = await fetch(url, {
        method: editingId ? 'PATCH' : 'POST', // El router complex usa PATCH para actualizar
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify(form)
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Ocurrió un error');
      
      Swal.fire({ icon: 'success', title: editingId ? '¡Actualizado!' : '¡Registrado!', confirmButtonColor: '#e11d48', timer: 1500, timerProgressBar: true });
      setForm({ nombre_completo: '', documento: '', telefono: '', tipo: 'temporal' });
      setEditingId(null);
      fetchJornaleros();
    } catch (err) {
      Swal.fire('Error', err.message, 'error');
    }
  };

  const handleEdit = (jornalero) => {
    setForm({
      nombre_completo: jornalero.nombre_completo,
      documento: jornalero.documento,
      telefono: jornalero.telefono || '',
      tipo: jornalero.tipo
    });
    setEditingId(jornalero.id);
  };

  const handleCancelEdit = () => {
    setForm({ nombre_completo: '', documento: '', telefono: '', tipo: 'temporal' });
    setEditingId(null);
  };

  const handleDelete = async (id) => {
    Swal.fire({
      title: '¿Desactivar jornalero?',
      text: "El trabajador será eliminado del sistema.",
      icon: 'warning', showCancelButton: true,
      confirmButtonColor: '#d33', cancelButtonColor: '#64748b',
      confirmButtonText: 'Sí, eliminar', cancelButtonText: 'Cancelar'
    }).then(async (result) => {
      if (result.isConfirmed) {
        try {
          await fetch(`http://localhost:8000/api/v1/jornaleros/${id}`, { method: 'DELETE', headers: { 'Authorization': `Bearer ${token}` } });
          Swal.fire('¡Eliminado!', 'El jornalero fue eliminado.', 'success');
          fetchJornaleros();
        } catch (err) { Swal.fire('Error', 'No se pudo eliminar.', 'error'); }
      }
    });
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-rose-700">Gestión de Jornaleros 👷‍♂️</h1>
        <p className="text-slate-500">Registra los trabajadores que laboran en tu finca.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="md:col-span-1">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
            <h2 className="text-xl font-semibold text-slate-800 mb-4">{editingId ? 'Editar Jornalero' : 'Nuevo Jornalero'}</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Nombre Completo</label>
                <input type="text" required value={form.nombre_completo} onChange={(e) => setForm({...form, nombre_completo: e.target.value})} className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-rose-500" placeholder="Juan Pérez" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Documento / C.C</label>
                <input type="text" required value={form.documento} onChange={(e) => setForm({...form, documento: e.target.value})} className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-rose-500" placeholder="123456789" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Teléfono</label>
                <input type="text" value={form.telefono} onChange={(e) => setForm({...form, telefono: e.target.value})} className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-rose-500" placeholder="3001234567" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Tipo de Contrato</label>
                <select value={form.tipo} onChange={(e) => setForm({...form, tipo: e.target.value})} className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-rose-500 bg-white">
                  <option value="temporal">Temporal (Por día/diario)</option>
                  <option value="fijo">Fijo (Mensual)</option>
                  <option value="contratista">Contratista</option>
                </select>
              </div>
              <div className="flex gap-2">
                <button type="submit" className="w-full bg-rose-600 text-white py-2 rounded-lg font-semibold hover:bg-rose-700">
                  {editingId ? '✓ Actualizar' : '+ Crear Jornalero'}
                </button>
                {editingId && (
                  <button type="button" onClick={handleCancelEdit} className="bg-slate-200 text-slate-700 px-4 py-2 rounded-lg font-semibold hover:bg-slate-300">✕</button>
                )}
              </div>
            </form>
          </div>
        </div>

        <div className="md:col-span-2">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
            <h2 className="text-xl font-semibold text-slate-800 mb-4">Lista de Trabajadores</h2>
            {loading ? <p className="text-slate-400">Cargando...</p> : jornaleros.length === 0 ? <p className="text-slate-400 italic">No hay jornaleros registrados.</p> : (
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-slate-50 border-b border-slate-200">
                    <tr>
                      <th className="px-4 py-3 font-semibold text-slate-600">Nombre</th>
                      <th className="px-4 py-3 font-semibold text-slate-600">Documento</th>
                      <th className="px-4 py-3 font-semibold text-slate-600">Teléfono</th>
                      <th className="px-4 py-3 font-semibold text-slate-600">Tipo</th>
                      <th className="px-4 py-3 font-semibold text-slate-600 text-right">Acciones</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {jornaleros.map((jornalero) => (
                      <tr key={jornalero.id} className="hover:bg-slate-50">
                        <td className="px-4 py-3 font-medium text-slate-800">{jornalero.nombre_completo}</td>
                        <td className="px-4 py-3 text-slate-500">{jornalero.documento}</td>
                        <td className="px-4 py-3 text-slate-500">{jornalero.telefono || '—'}</td>
                        <td className="px-4 py-3">
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${jornalero.tipo === 'fijo' ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700'}`}>
                            {jornalero.tipo}
                          </span>
                        </td>
                        <td className="px-4 py-3 text-right whitespace-nowrap">
                          <button onClick={() => handleEdit(jornalero)} className="text-sky-600 hover:text-sky-800 font-medium mr-3">Editar</button>
                          <button onClick={() => handleDelete(jornalero.id)} className="text-red-500 hover:text-red-700 font-medium">Eliminar</button>
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