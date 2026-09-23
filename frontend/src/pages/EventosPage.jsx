import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Swal from 'sweetalert2';

export default function EventosPage() {
  const navigate = useNavigate();
  const [eventos, setEventos] = useState([]);
  const [lotes, setLotes] = useState([]);
  const [insumos, setInsumos] = useState([]);
  const [form, setForm] = useState({ lote_id: '', insumo_id: '', cantidad: 1, descripcion: 'Aplicación de insumo' });
  const [loading, setLoading] = useState(true);

  const token = localStorage.getItem('agroflow_token');

  const fetchAllData = async () => {
    try {
      const headers = { 'Authorization': `Bearer ${token}` };
      const [resEventos, resLotes, resInsumos] = await Promise.all([
        fetch('http://localhost:8000/api/v1/eventos/', { headers }),
        fetch('http://localhost:8000/api/v1/lotes/', { headers }),
        fetch('http://localhost:8000/api/v1/insumos/', { headers })
      ]);

      const dataEventos = resEventos.ok ? await resEventos.json() : [];
      const dataLotes = resLotes.ok ? await resLotes.json() : [];
      const dataInsumos = resInsumos.ok ? await resInsumos.json() : [];

      setEventos(dataEventos);
      setLotes(dataLotes);
      setInsumos(dataInsumos);

      if (dataLotes.length > 0) setForm(prev => ({ ...prev, lote_id: dataLotes[0].id }));
      if (dataInsumos.length > 0) setForm(prev => ({ ...prev, insumo_id: dataInsumos[0].id }));

    } catch (err) {
      Swal.fire('Error', 'No se pudieron cargar los datos', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!token) { navigate('/login'); return; }
    fetchAllData();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch('http://localhost:8000/api/v1/eventos/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify(form)
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Ocurrió un error');
      
      Swal.fire({
        icon: 'success',
        title: '¡Evento Registrado!',
        html: `Insumo aplicado y stock actualizado.<br><b>Costo generado: $${Number(data.costo_total).toLocaleString('es-CO')}</b>`,
        confirmButtonColor: '#7c3aed'
      });
      
      setForm(prev => ({ ...prev, cantidad: 1, descripcion: 'Aplicación de insumo' }));
      fetchAllData();
    } catch (err) {
      Swal.fire('Error', err.message, 'error');
    }
  };

  const handleDelete = async (id) => {
    Swal.fire({
      title: '¿Anular evento?',
      text: "El stock del insumo será devuelto a la bodega.",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#d33',
      cancelButtonColor: '#64748b',
      confirmButtonText: 'Sí, eliminar'
    }).then(async (result) => {
      if (result.isConfirmed) {
        try {
          await fetch(`http://localhost:8000/api/v1/eventos/${id}`, { method: 'DELETE', headers: { 'Authorization': `Bearer ${token}` } });
          Swal.fire('¡Anulado!', 'El evento fue eliminado y el stock devuelto.', 'success');
          fetchAllData();
        } catch (err) { Swal.fire('Error', 'No se pudo eliminar.', 'error'); }
      }
    });
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-violet-700">Eventos Agrícolas 🌩️</h1>
        <p className="text-slate-500">Aplica insumos a tus lotes y calcula costos automáticamente.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        
        {/* Formulario de Evento */}
        <div className="md:col-span-1">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
            <h2 className="text-xl font-semibold text-slate-800 mb-4">Nuevo Evento</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Lote (Destino)</label>
                <select 
                  value={form.lote_id}
                  onChange={(e) => setForm({...form, lote_id: e.target.value})}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-violet-500 bg-white"
                  required
                >
                  {lotes.map(l => <option key={l.id} value={l.id}>{l.nombre}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Insumo a Aplicar</label>
                <select 
                  value={form.insumo_id}
                  onChange={(e) => setForm({...form, insumo_id: e.target.value})}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-violet-500 bg-white"
                  required
                >
                  {insumos.map(i => <option key={i.id} value={i.id}>{i.nombre} (Stock: {i.stock_actual} {i.unidad_medida})</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Cantidad a Aplicar</label>
                <input 
                  type="number" required step="0.1" min="0.1"
                  value={form.cantidad}
                  onChange={(e) => setForm({...form, cantidad: parseFloat(e.target.value)})}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-violet-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Descripción (Opcional)</label>
                <input 
                  type="text"
                  value={form.descripcion}
                  onChange={(e) => setForm({...form, descripcion: e.target.value})}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-violet-500"
                />
              </div>
              <button type="submit" className="w-full bg-violet-600 text-white py-2 rounded-lg font-semibold hover:bg-violet-700">
                ⚡ Aplicar Insumo
              </button>
            </form>
          </div>
        </div>

        {/* Historial de Eventos */}
        <div className="md:col-span-2">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
            <h2 className="text-xl font-semibold text-slate-800 mb-4">Historial de Costos por Lote</h2>
            {loading ? <p className="text-slate-400">Cargando...</p> : eventos.length === 0 ? <p className="text-slate-400 italic">No hay eventos registrados.</p> : (
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-slate-50 border-b border-slate-200">
                    <tr>
                      <th className="px-4 py-3 font-semibold text-slate-600">Fecha</th>
                      <th className="px-4 py-3 font-semibold text-slate-600">Descripción</th>
                      <th className="px-4 py-3 font-semibold text-slate-600">Cantidad</th>
                      <th className="px-4 py-3 font-semibold text-slate-600">Costo Total</th>
                      <th className="px-4 py-3 font-semibold text-slate-600 text-right">Acción</th> {/* NUEVA COLUMNA */}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {eventos.map((ev) => {
                      const cant = Number(ev.cantidad);
                      const formattedCant = cant % 1 === 0 ? cant : cant.toFixed(2);
                      const costo = Number(ev.costo_total);
                      const formattedCosto = `$${costo.toLocaleString('es-CO')}`;

                      return (
                        <tr key={ev.id} className="hover:bg-slate-50">
                          <td className="px-4 py-3 text-slate-500">{ev.fecha}</td>
                          <td className="px-4 py-3 font-medium text-slate-800">{ev.descripcion}</td>
                          <td className="px-4 py-3 text-slate-600 font-medium">
                            {formattedCant} <span className="text-xs text-slate-400">{ev.unidad_medida}</span>
                          </td>
                          <td className="px-4 py-3 font-bold text-violet-600">
                            {formattedCosto}
                          </td>
                          {/* === BOTÓN ELIMINAR === */}
                          <td className="px-4 py-3 text-right">
                            <button onClick={() => handleDelete(ev.id)} className="text-red-500 hover:text-red-700 font-medium">Eliminar</button>
                          </td>
                          {/* ======================= */}
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