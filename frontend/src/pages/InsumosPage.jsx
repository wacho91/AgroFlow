import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export default function InsumosPage() {
  const navigate = useNavigate();
  const [insumos, setInsumos] = useState([]);
  const [form, setForm] = useState({ nombre: '', codigo: '', unidad_medida: 'kg', stock_actual: 0, stock_minimo: 0 });
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const token = localStorage.getItem('agroflow_token');

  const fetchInsumos = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/v1/insumos/', { headers: { 'Authorization': `Bearer ${token}` } });
      const data = await res.json();
      setInsumos(data);
    } catch (err) { setError('Error al cargar insumos'); } 
    finally { setLoading(false); }
  };

  useEffect(() => { if (!token) { navigate('/login'); return; } fetchInsumos(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    const method = editingId ? 'PUT' : 'POST';
    const url = editingId ? `http://localhost:8000/api/v1/insumos/${editingId}` : 'http://localhost:8000/api/v1/insumos/';
    try {
      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify(form)
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Error al guardar el insumo');
      setForm({ nombre: '', codigo: '', unidad_medida: 'kg', stock_actual: 0, stock_minimo: 0 });
      setEditingId(null);
      fetchInsumos();
    } catch (err) { setError(err.message); }
  };

  const handleEdit = (insumo) => { setForm(insumo); setEditingId(insumo.id); };
  const handleCancelEdit = () => { setForm({ nombre: '', codigo: '', unidad_medida: 'kg', stock_actual: 0, stock_minimo: 0 }); setEditingId(null); };
  const handleDelete = async (id) => {
    if (!window.confirm("¿Eliminar este insumo?")) return;
    try {
      await fetch(`http://localhost:8000/api/v1/insumos/${id}`, { method: 'DELETE', headers: { 'Authorization': `Bearer ${token}` } });
      fetchInsumos();
    } catch (err) { setError("Error al eliminar"); }
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-sky-700">Gestión de Insumos 🧪</h1>
        <p className="text-slate-500">Controla tu bodega de fertilizantes, semillas y químicos.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="md:col-span-1">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
            <h2 className="text-xl font-semibold text-slate-800 mb-4">{editingId ? 'Editar Insumo' : 'Nuevo Insumo'}</h2>
            {error && <div className="bg-red-50 text-red-600 p-2 rounded mb-4 text-sm">{error}</div>}
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Nombre</label>
                <input type="text" required value={form.nombre} onChange={(e) => setForm({...form, nombre: e.target.value})} className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500" placeholder="Fertilizante NPK 15-15-15" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Código / SKU</label>
                <input type="text" required value={form.codigo} onChange={(e) => setForm({...form, codigo: e.target.value})} className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500" placeholder="FER-001" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Unidad de Medida</label>
                <select value={form.unidad_medida} onChange={(e) => setForm({...form, unidad_medida: e.target.value})} className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500 bg-white">
                  <option value="kg">Kilogramos (kg)</option>
                  <option value="lt">Litros (lt)</option>
                  <option value="und">Unidades (und)</option>
                </select>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-sm font-medium text-slate-600 mb-1">Stock Inicial</label>
                  <input type="number" required step="0.1" value={form.stock_actual} onChange={(e) => setForm({...form, stock_actual: parseFloat(e.target.value)})} className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-600 mb-1">Stock Mínimo</label>
                  <input type="number" required step="0.1" value={form.stock_minimo} onChange={(e) => setForm({...form, stock_minimo: parseFloat(e.target.value)})} className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500" />
                </div>
              </div>
              <div className="flex gap-2">
                <button type="submit" className="w-full bg-sky-600 text-white py-2 rounded-lg font-semibold hover:bg-sky-700">
                  {editingId ? '✓ Actualizar' : '+ Crear Insumo'}
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
            <h2 className="text-xl font-semibold text-slate-800 mb-4">Inventario de Bodega</h2>
            {loading ? <p className="text-slate-400">Cargando...</p> : insumos.length === 0 ? <p className="text-slate-400 italic">Bodega vacía.</p> : (
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-slate-50 border-b border-slate-200">
                    <tr>
                      <th className="px-4 py-3 font-semibold text-slate-600">Código</th>
                      <th className="px-4 py-3 font-semibold text-slate-600">Nombre</th>
                      <th className="px-4 py-3 font-semibold text-slate-600">Stock Actual</th>
                      <th className="px-4 py-3 font-semibold text-slate-600">Alerta</th>
                      <th className="px-4 py-3 font-semibold text-slate-600 text-right">Acciones</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {insumos.map((insumo) => {
                      const stockActual = Number(insumo.stock_actual);
                      const stockMinimo = Number(insumo.stock_minimo);
                      const isLow = stockActual <= stockMinimo;
                      const formattedStock = stockActual % 1 === 0 ? stockActual : stockActual.toFixed(2);

                      return (
                        <tr key={insumo.id} className="hover:bg-slate-50">
                          <td className="px-4 py-3 font-medium text-slate-800">{insumo.codigo}</td>
                          <td className="px-4 py-3 text-slate-600">{insumo.nombre}</td>
                          <td className="px-4 py-3 text-slate-800 font-medium">
                            {formattedStock} <span className="text-xs text-slate-400">{insumo.unidad_medida}</span>
                            <span className="block text-xs text-slate-400">(Mín: {stockMinimo})</span>
                          </td>
                          <td className="px-4 py-3">
                            {isLow ? <span className="bg-red-100 text-red-700 px-2 py-1 rounded-full text-xs font-bold">⚠️ Reabastecer</span> : <span className="bg-green-100 text-green-700 px-2 py-1 rounded-full text-xs font-medium">Óptimo</span>}
                          </td>
                          <td className="px-4 py-3 text-right whitespace-nowrap">
                            <button onClick={() => handleEdit(insumo)} className="text-sky-600 hover:text-sky-800 font-medium mr-3">Editar</button>
                            <button onClick={() => handleDelete(insumo.id)} className="text-red-500 hover:text-red-700 font-medium">Eliminar</button>
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
  );
}