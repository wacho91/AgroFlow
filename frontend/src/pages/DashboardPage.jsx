import { useState, useEffect } from 'react';

export default function DashboardPage() {
  const [fincaCount, setFincaCount] = useState(0);
  const [loteCount, setLoteCount] = useState(0);
  const [insumoCount, setInsumoCount] = useState(0);
  
  const token = localStorage.getItem('agroflow_token');

  useEffect(() => {
    if (!token) return; // El AppLayout ya maneja la redirección si no hay token
    
    const fetchStats = async () => {
      try {
        const headers = { 'Authorization': `Bearer ${token}` };
        
        const [resFincas, resLotes, resInsumos] = await Promise.all([
          fetch('http://localhost:8000/api/v1/fincas/', { headers }),
          fetch('http://localhost:8000/api/v1/lotes/', { headers }),
          fetch('http://localhost:8000/api/v1/insumos/', { headers })
        ]);

        if (resFincas.ok) setFincaCount((await resFincas.json()).length);
        if (resLotes.ok) setLoteCount((await resLotes.json()).length);
        if (resInsumos.ok) setInsumoCount((await resInsumos.json()).length);

      } catch (err) {
        console.error("Error al cargar estadísticas");
      }
    };
    
    fetchStats();
  }, [token]);

  return (
    <div>
      <h1 className="text-3xl font-bold text-slate-800 mb-2">Dashboard 🌱</h1>
      <p className="text-slate-500 mb-8">Resumen operativo de tu finca.</p>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
          <p className="text-sm text-emerald-600 font-medium mb-1">Fincas Registradas</p>
          <p className="text-4xl font-bold text-emerald-800">{fincaCount}</p>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
          <p className="text-sm text-amber-600 font-medium mb-1">Lotes Activos</p>
          <p className="text-4xl font-bold text-amber-800">{loteCount}</p>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
          <p className="text-sm text-sky-600 font-medium mb-1">Insumos en Bodega</p>
          <p className="text-4xl font-bold text-sky-800">{insumoCount}</p>
        </div>
      </div>
    </div>
  );
}