import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Swal from 'sweetalert2';

export default function TesoreriaPage() {
  const navigate = useNavigate();
  const [movimientos, setMovimientos] = useState([]);
  const [form, setForm] = useState({ fecha: new Date().toISOString().slice(0,10), tipo: 'ingreso', concepto: '', monto: 0 });
  const [loading, setLoading] = useState(true);

  const token = localStorage.getItem('agroflow_token');

  const fetchMovimientos = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/v1/tesoreria/', { headers: { 'Authorization': `Bearer ${token}` } });
      const data = await res.json();
      setMovimientos(data);
    } catch (err) {
      Swal.fire('Error', 'No se pudieron cargar los movimientos', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { if (!token) { navigate('/login'); return; } fetchMovimientos(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch('http://localhost:8000/api/v1/tesoreria/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify(form)
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Ocurrió un error');
      
      Swal.fire({
        icon: 'success',
        title: '¡Registrado!',
        text: 'El movimiento de tesorería ha sido guardado.',
        confirmButtonColor: '#0284c7',
        timer: 1500,
        timerProgressBar: true
      });
      
      setForm({ fecha: new Date().toISOString().slice(0,10), tipo: 'ingreso', concepto: '', monto: 0 });
      fetchMovimientos();
    } catch (err) {
      Swal.fire('Error', err.message, 'error');
    }
  };

  const handleDelete = async (id) => {
    Swal.fire({
      title: '¿Anular movimiento?',
      text: "El registro financiero será eliminado.",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#d33',
      cancelButtonColor: '#64748b',
      confirmButtonText: 'Sí, eliminar',
      cancelButtonText: 'Cancelar'
    }).then(async (result) => {
      if (result.isConfirmed) {
        try {
          await fetch(`http://localhost:8000/api/v1/tesoreria/${id}`, { method: 'DELETE', headers: { 'Authorization': `Bearer ${token}` } });
          Swal.fire('¡Eliminado!', 'El movimiento fue eliminado.', 'success');
          fetchMovimientos();
        } catch (err) {
          Swal.fire('Error', 'No se pudo eliminar.', 'error');
        }
      }
    });
  };

  const formatCurrency = (value) => `$${Number(value).toLocaleString('es-CO')}`;

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-indigo-700">Tesorería y Caja 💰</h1>
        <p className="text-slate-500">Registra tus ingresos por ventas y tus egresos operativos.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* Formulario */}
        <div className="md:col-span-1">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
            <h2 className="text-xl font-semibold text-slate-800 mb-4">Nuevo Movimiento</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Fecha</label>
                <input type="date" required value={form.fecha} onChange={(e) => setForm({...form, fecha: e.target.value})} className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Tipo de Movimiento</label>
                <select value={form.tipo} onChange={(e) => setForm({...form, tipo: e.target.value})} className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 bg-white">
                  <option value="ingreso">Ingreso (Venta, Cobro)</option>
                  <option value="egreso">Egreso (Compra, Pago)</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Concepto</label>
                <input type="text" required value={form.concepto} onChange={(e) => setForm({...form, concepto: e.target.value})} className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500" placeholder="Venta de 100kg de café" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Monto (COP)</label>
                <input type="number" required value={form.monto} onChange={(e) => setForm({...form, monto: parseFloat(e.target.value)})} className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500" placeholder="0" />
              </div>
              <button type="submit" className="w-full bg-indigo-600 text-white py-2 rounded-lg font-semibold hover:bg-indigo-700">
                + Registrar Movimiento
              </button>
            </form>
          </div>
        </div>

        {/* Lista de Movimientos */}
        <div className="md:col-span-2">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
            <h2 className="text-xl font-semibold text-slate-800 mb-4">Historial de Caja</h2>
            {loading ? <p className="text-slate-400">Cargando...</p> : movimientos.length === 0 ? <p className="text-slate-400 italic">No hay movimientos registrados.</p> : (
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-slate-50 border-b border-slate-200">
                    <tr>
                      <th className="px-4 py-3 font-semibold text-slate-600">Fecha</th>
                      <th className="px-4 py-3 font-semibold text-slate-600">Concepto</th>
                      <th className="px-4 py-3 font-semibold text-slate-600">Tipo</th>
                      <th className="px-4 py-3 font-semibold text-slate-600">Monto</th>
                      <th className="px-4 py-3 font-semibold text-slate-600 text-right">Acción</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {movimientos.map((mov) => (
                      <tr key={mov.id} className="hover:bg-slate-50">
                        <td className="px-4 py-3 text-slate-500">{mov.fecha}</td>
                        <td className="px-4 py-3 font-medium text-slate-800">{mov.concepto}</td>
                        <td className="px-4 py-3">
                          {mov.tipo === 'ingreso' ? (
                            <span className="bg-emerald-100 text-emerald-700 px-2 py-1 rounded-full text-xs font-bold">Ingreso</span>
                          ) : (
                            <span className="bg-red-100 text-red-700 px-2 py-1 rounded-full text-xs font-bold">Egreso</span>
                          )}
                        </td>
                        <td className={`px-4 py-3 font-bold ${mov.tipo === 'ingreso' ? 'text-emerald-600' : 'text-red-600'}`}>
                          {mov.tipo === 'ingreso' ? '+' : '-'} {formatCurrency(mov.monto)}
                        </td>
                        <td className="px-4 py-3 text-right">
                          <button onClick={() => handleDelete(mov.id)} className="text-red-500 hover:text-red-700 font-medium">Eliminar</button>
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