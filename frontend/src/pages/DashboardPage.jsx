import { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from 'recharts';

export default function DashboardPage() {
  const [stats, setStats] = useState({ fincas: 0, lotes: 0, insumos: 0, cultivos: 0 });
  const token = localStorage.getItem('agroflow_token');

  useEffect(() => {
    if (!token) return;
    const fetchStats = async () => {
      try {
        const headers = { 'Authorization': `Bearer ${token}` };
        const [resFincas, resLotes, resInsumos, resCultivos] = await Promise.all([
          fetch('http://localhost:8000/api/v1/fincas/', { headers }),
          fetch('http://localhost:8000/api/v1/lotes/', { headers }),
          fetch('http://localhost:8000/api/v1/insumos/', { headers }),
          fetch('http://localhost:8000/api/v1/cultivos/', { headers })
        ]);

        const dataFincas = resFincas.ok ? await resFincas.json() : [];
        const dataLotes = resLotes.ok ? await resLotes.json() : [];
        const dataInsumos = resInsumos.ok ? await resInsumos.json() : [];
        const dataCultivos = resCultivos.ok ? await resCultivos.json() : [];

        setStats({
          fincas: dataFincas.length,
          lotes: dataLotes.length,
          insumos: dataInsumos.length,
          cultivos: dataCultivos.length
        });
      } catch (err) {
        console.error("Error al cargar estadísticas");
      }
    };
    fetchStats();
  }, [token]);

  // === Datos Financieros (Simulados por ahora) ===
  const dataBalance = [
    { name: 'Ene', Ingresos: 12000000, Egresos: 8000000 },
    { name: 'Feb', Ingresos: 15000000, Egresos: 9000000 },
    { name: 'Mar', Ingresos: 18000000, Egresos: 12000000 },
    { name: 'Abr', Ingresos: 14000000, Egresos: 7000000 },
    { name: 'May', Ingresos: 22000000, Egresos: 11000000 },
  ];

  const dataGastos = [
    { name: 'Insumos', value: 4500000 },
    { name: 'Jornales', value: 3200000 },
    { name: 'Maquinaria', value: 1500000 },
    { name: 'Otros', value: 800000 },
  ];
  
  const COLORS = ['#10b981', '#f59e0b', '#0ea5e9', '#ef4444'];
  const formatCurrency = (value) => `$${value.toLocaleString('es-CO')}`;

  return (
    <div>
      <h1 className="text-3xl font-bold text-slate-800 mb-2">Dashboard Financiero 📊</h1>
      <p className="text-slate-500 mb-8">Resumen operativo y financiero de tu finca.</p>
      
      {/* KPIs Operativos (Pequeños) */}
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
        {/* Gráfica de Barras (Ingresos vs Egresos) */}
        <div className="md:col-span-2 bg-white p-6 rounded-xl shadow-sm border border-slate-200">
          <h2 className="text-lg font-semibold text-slate-800 mb-4">Balance de Ingresos vs Egresos</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={dataBalance}>
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

        {/* Gráfica de Pastel (Distribución de Gastos) */}
        <div className="md:col-span-1 bg-white p-6 rounded-xl shadow-sm border border-slate-200">
          <h2 className="text-lg font-semibold text-slate-800 mb-4">Distribución de Gastos</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie data={dataGastos} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label>
                {dataGastos.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip formatter={(v) => formatCurrency(v)} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Tarjeta de Balance Neto */}
      <div className="bg-gradient-to-r from-emerald-600 to-teal-600 p-6 rounded-xl shadow-lg text-white flex flex-col md:flex-row justify-between items-center">
        <div className="mb-4 md:mb-0">
          <p className="text-emerald-100 font-medium text-sm uppercase">Balance Neto del Mes</p>
          <p className="text-4xl font-bold">{formatCurrency(11000000)}</p>
        </div>
        <div className="text-right">
          <p className="text-emerald-100 text-sm uppercase">Crecimiento vs Mes Anterior</p>
          <p className="text-3xl font-bold">+15% 📈</p>
        </div>
      </div>
    </div>
  );
}