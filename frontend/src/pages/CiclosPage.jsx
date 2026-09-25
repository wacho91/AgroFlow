import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Swal from 'sweetalert2';

export default function CiclosPage() {
  const navigate = useNavigate();
  const [ciclos, setCiclos] = useState([]);
  const [lotes, setLotes] = useState([]);
  const [cultivos, setCultivos] = useState([]);
  const [form, setForm] = useState({ lote_id: '', cultivo_id: '', codigo: '', area_sembrada_ha: 1 });
  const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);

  const token = localStorage.getItem('agroflow_token');

  const fetchAllData = async () => {
    try {
      const headers = { 'Authorization': `Bearer ${token}` };
      const [resCiclos, resLotes, resCultivos] = await Promise.all([
        fetch('http://localhost:8000/api/v1/ciclos/', { headers }),
        fetch('http://localhost:8000/api/v1/lotes/', { headers }),
        fetch('http://localhost:8000/api/v1/cultivos/', { headers })
      ]);

      const dataCiclos = resCiclos.ok ? await resCiclos.json() : [];
      const dataLotes = resLotes.ok ? await resLotes.json() : [];
      const dataCultivos = resCultivos.ok ? await resCultivos.json() : [];

      setCiclos(dataCiclos);
      setLotes(dataLotes);
      setCultivos(dataCultivos);

      if (dataLotes.length > 0) setForm(prev => ({ ...prev, lote_id: dataLotes[0].id }));
      if (dataCultivos.length > 0) setForm(prev => ({ ...prev, cultivo_id: dataCultivos[0].id }));

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
    setSaving(true); // Bloqueamos
    try {
      const res = await fetch('http://localhost:8000/api/v1/ciclos/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify(form)
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Ocurrió un error');
      
      Swal.fire({
        icon: 'success',
        title: '¡Siembra Iniciada!',
        text: 'El ciclo productivo ha comenzado. Los costos se empezarán a acumular aquí.',
        confirmButtonColor: '#4f46e5'
      });
      
      setForm(prev => ({ ...prev, codigo: '', area_sembrada_ha: 1 }));
      fetchAllData();
    } catch (err) {
      Swal.fire('Error', err.message, 'error');
    } finally {
      setSaving(false); // Desbloqueamos
    }
  };

  const formatCurrency = (value) => `$${Number(value).toLocaleString('es-CO')}`;

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-indigo-700">Ciclos Productivos (Siembras) 📅</h1>
        <p className="text-slate-500">Inicia la siembra de tus lotes y mide la rentabilidad en tiempo real.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="md:col-span-1">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
            <h2 className="text-xl font-semibold text-slate-800 mb-4">Iniciar Nuevo Ciclo</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Lote a Sembrar</label>
                <select 
                  value={form.lote_id}
                  onChange={(e) => setForm({...form, lote_id: e.target.value})}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 bg-white"
                  required
                >
                  {lotes.map(l => <option key={l.id} value={l.id}>{l.nombre}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Cultivo</label>
                <select 
                  value={form.cultivo_id}
                  onChange={(e) => setForm({...form, cultivo_id: e.target.value})}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 bg-white"
                  required
                >
                  {cultivos.map(c => <option key={c.id} value={c.id}>{c.nombre}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Código del Ciclo</label>
                <input 
                  type="text" required
                  value={form.codigo}
                  onChange={(e) => setForm({...form, codigo: e.target.value})}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                  placeholder="CIC-001"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1">Área a Sembrar (ha)</label>
                <input 
                  type="number" required step="0.1" min="0.1"
                  value={form.area_sembrada_ha}
                  onChange={(e) => setForm({...form, area_sembrada_ha: parseFloat(e.target.value)})}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                />
              </div>
                <button type="submit" disabled={saving} className="w-full bg-indigo-600 text-white py-2 rounded-lg font-semibold hover:bg-indigo-700 disabled:opacity-50">
                    {saving ? 'Iniciando...' : '🌱 Iniciar Siembra'}
              </button>
            </form>
          </div>
        </div>

        <div className="md:col-span-2">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
            <h2 className="text-xl font-semibold text-slate-800 mb-4">Ciclos Activos y Cerrados</h2>
            {loading ? <p className="text-slate-400">Cargando...</p> : ciclos.length === 0 ? <p className="text-slate-400 italic">No hay ciclos productivos iniciados.</p> : (
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-slate-50 border-b border-slate-200">
                    <tr>
                      <th className="px-4 py-3 font-semibold text-slate-600">Código</th>
                      <th className="px-4 py-3 font-semibold text-slate-600">Cultivo</th>
                      <th className="px-4 py-3 font-semibold text-slate-600">Estado</th>
                      <th className="px-4 py-3 font-semibold text-slate-600">Costos</th>
                      <th className="px-4 py-3 font-semibold text-slate-600">Ingresos</th>
                      <th className="px-4 py-3 font-semibold text-slate-600">Margen</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {ciclos.map((ciclo) => {
                      const margen = Number(ciclo.margen_bruto);
                      const margenColor = margen >= 0 ? 'text-emerald-600' : 'text-red-600';

                      return (
                        <tr key={ciclo.id} className="hover:bg-slate-50">
                          <td className="px-4 py-3 font-medium text-slate-800">{ciclo.codigo}</td>
                          <td className="px-4 py-3 text-slate-600">{ciclo.nombre}</td>
                          <td className="px-4 py-3">
                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${ciclo.estado === 'en_curso' ? 'bg-sky-100 text-sky-700' : 'bg-slate-100 text-slate-600'}`}>
                              {ciclo.estado.replace('_', ' ')}
                            </span>
                          </td>
                          <td className="px-4 py-3 text-red-500 font-medium">{formatCurrency(ciclo.costo_total)}</td>
                          <td className="px-4 py-3 text-emerald-500 font-medium">{formatCurrency(ciclo.ingreso_total)}</td>
                          <td className={`px-4 py-3 font-bold ${margenColor}`}>
                            {formatCurrency(margen)}
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