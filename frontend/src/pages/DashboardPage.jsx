import { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from 'recharts';

export default function DashboardPage() {
  const [stats, setStats] = useState({ fincas: 0, lotes: 0, insumos: 0, cultivos: 0 });
  const [finanzas, setFinanzas] = useState({ ingresos: 0, egresos: 0, balance: 0, dataBalance: [], dataGastos: [] });
  const [climas, setClimas] = useState([]); // Ahora es una lista de climas
  const token = localStorage.getItem('agroflow_token');

  useEffect(() => {
    if (!token) return;
    const fetchAll = async () => {
      try {
        const headers = { 'Authorization': `Bearer ${token}` };
        
        const [resFincas, resLotes, resInsumos, resCultivos, resFin, resClima] = await Promise.all([
          fetch('http://localhost:8000/api/v1/fincas/', { headers }),
          fetch('http://localhost:8000/api/v1/lotes/', { headers }),
          fetch('http://localhost:8000/api/v1/insumos/', { headers }),
          fetch('http://localhost:8000/api/v1/cultivos/', { headers }),
          fetch('http://localhost:8000/api/v1/tesoreria/', { headers }),
          fetch('http://localhost:8000/api/v1/clima/', { headers })
        ]);

        const dataFincas = resFincas.ok ? await resFincas.json() : [];
        const dataLotes = resLotes.ok ? await resLotes.json() : [];
        const dataInsumos = resInsumos.ok ? await resInsumos.json() : [];
        const dataCultivos = resCultivos.ok ? await resCultivos.json() : [];
        const dataFin = resFin.ok ? await resFin.json() : [];
        
        if (resClima.ok) {
          const dataClima = await resClima.json();
          setClimas(dataClima);
        }

        setStats({
          fincas: dataFincas.length,
          lotes: dataLotes.length,
          insumos: dataInsumos.length,
          cultivos: dataCultivos.length
        });

        let totalIngresos = 0, totalEgresos = 0;
        const mesesMap = {}, gastosMap = {};
        const nombresMeses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];

        dataFin.forEach(mov => {
          const monto = Number(mov.monto);
          const fecha = new Date(mov.fecha + 'T00:00:00');
          const mesKey = `${fecha.getFullYear()}-${String(fecha.getMonth() + 1).padStart(2, '0')}`;
          const mesNombre = nombresMeses[fecha.getMonth()];

          if (!mesesMap[mesKey]) mesesMap[mesKey] = { name: mesNombre, Ingresos: 0, Egresos: 0 };

          if (mov.tipo === 'ingreso') {
            totalIngresos += monto;
            mesesMap[mesKey].Ingresos += monto;
          } else {
            totalEgresos += monto;
            mesesMap[mesKey].Egresos += monto;
            gastosMap[mov.concepto] = (gastosMap[mov.concepto] || 0) + monto;
          }
        });

        const dataBalance = Object.values(mesesMap).sort((a, b) => a.name > b.name ? 1 : -1);
        const dataGastos = Object.keys(gastosMap).map(k => ({ name: k, value: gastosMap[k] }));

        setFinanzas({
          ingresos: totalIngresos,
          egresos: totalEgresos,
          balance: totalIngresos - totalEgresos,
          dataBalance,
          dataGastos
        });

      } catch (err) {
        console.error("Error al cargar datos:", err);
      }
    };
    fetchAll();
  }, [token]);

  const COLORS = ['#10b981', '#f59e0b', '#0ea5e9', '#ef4444', '#8b5cf6', '#ec4899'];
  const formatCurrency = (value) => `$${value.toLocaleString('es-CO')}`;

  return (
    <div>
      <h1 className="text-3xl font-bold text-slate-800 mb-2">Dashboard Financiero 📊</h1>
      <p className="text-slate-500 mb-8">Resumen operativo y financiero de tu finca en tiempo real.</p>
      
      {/* === SLIDER DE TARJETAS DEL CLIMA === */}
      {climas.length > 0 && (
        <div className="mb-8 flex gap-6 overflow-x-auto pb-4">
          {climas.map((clima) => (
            <div key={clima.finca_id} className={`min-w-[300px] p-6 rounded-xl shadow-sm border flex-shrink-0 ${clima.alerta ? 'bg-amber-50 border-amber-200' : 'bg-sky-50 border-sky-200'}`}>
              <div className="flex items-center gap-4 mb-4">
                <img src={`http://openweathermap.org/img/wn/${clima.icono}@2x.png`} alt="Clima" className="w-16 h-16" />
                <div>
                  <p className="text-sm text-slate-500 font-medium">{clima.nombre_finca}</p>
                  <h2 className="text-2xl font-bold text-slate-800">{clima.temperatura}°C</h2>
                  <p className="text-xs text-slate-500">{clima.descripcion}</p>
                </div>
              </div>
              <div className="text-xs text-slate-500 mb-2">📍 {clima.municipio} | 💧 Humedad: {clima.humedad}%</div>
              {clima.alerta && (
                <div className="bg-red-100 text-red-700 px-3 py-2 rounded-lg font-semibold text-center text-xs">
                  {clima.alerta}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* KPIs Operativos */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-white p-4 rounded-xl shadow-sm border border-slate-200">
          <p className="text-xs text-emerald-600 font-medium mb-1 uppercase">Fincas</p>
          <p className="text-2xl font-bold text-slate-800">{stats.fincas}</p>
        </div>
        <div className="bg-white p-4 rounded-xl shadow-sm border border-slate-200">
          <p className="text-xs text-amber-600 font-medium mb-1 uppercase">Lotes</p>
          <p className="text-2xl font-bold text-slate-800">{stats.lotes}</p>
        </div>
        <div className="bg-white p-4 rounded-xl shadow-sm border border-slate-200">
          <p className="text-xs text-sky-600 font-medium mb-1 uppercase">Insumos</p>
          <p className="text-2xl font-bold text-slate-800">{stats.insumos}</p>
        </div>
        <div className="bg-white p-4 rounded-xl shadow-sm border border-slate-200">
          <p className="text-xs text-lime-600 font-medium mb-1 uppercase">Cultivos</p>
          <p className="text-2xl font-bold text-slate-800">{stats.cultivos}</p>
        </div>
      </div>

      {/* Gráficas Financieras */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="md:col-span-2 bg-white p-6 rounded-xl shadow-sm border border-slate-200">
          <h2 className="text-lg font-semibold text-slate-800 mb-4">Balance de Ingresos vs Egresos</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={finanzas.dataBalance}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="name" stroke="#64748b" fontSize={12} />
              <YAxis stroke="#64748b" fontSize={12} tickFormatter={(v) => `${v/1000000}M`} />
              <Tooltip formatter={(v) => formatCurrency(v)} />
              <Legend />
              <Bar dataKey="Ingresos" fill="#10b981" radius={[4, 4, 0, 0]} />
              <Bar dataKey="Egresos" fill="#ef4444" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="md:col-span-1 bg-white p-6 rounded-xl shadow-sm border border-slate-200">
          <h2 className="text-lg font-semibold text-slate-800 mb-4">Distribución de Gastos</h2>
          {finanzas.dataGastos.length === 0 ? (
            <div className="h-[300px] flex items-center justify-center text-slate-400 text-sm text-center">
              No hay egresos registrados aún.
            </div>
          ) : (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie data={finanzas.dataGastos} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label>
                  {finanzas.dataGastos.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(v) => formatCurrency(v)} />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

      {/* Tarjeta de Balance Neto Real */}
      <div className={`p-6 rounded-xl shadow-lg text-white flex flex-col md:flex-row justify-between items-center ${finanzas.balance >= 0 ? 'bg-gradient-to-r from-emerald-600 to-teal-600' : 'bg-gradient-to-r from-red-600 to-rose-600'}`}>
        <div className="mb-4 md:mb-0">
          <p className="text-white/80 font-medium text-sm uppercase">Balance Neto Total</p>
          <p className="text-4xl font-bold">{formatCurrency(finanzas.balance)}</p>
        </div>
        <div className="text-right">
          <p className="text-white/80 text-sm uppercase">Ingresos Totales</p>
          <p className="text-2xl font-bold text-emerald-100">{formatCurrency(finanzas.ingresos)}</p>
          <p className="text-white/80 text-sm uppercase mt-2">Egresos Totales</p>
          <p className="text-2xl font-bold text-red-100">{formatCurrency(finanzas.egresos)}</p>
        </div>
      </div>
    </div>
  );
}