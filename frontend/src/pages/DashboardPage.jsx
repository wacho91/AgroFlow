import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';

export default function DashboardPage() {
  const navigate = useNavigate();
  const [fincaCount, setFincaCount] = useState(0);
  
  const token = localStorage.getItem('agroflow_token');

  const handleLogout = () => {
    localStorage.removeItem('agroflow_token');
    navigate('/login');
  };

  // === MAGIA: Pedimos a la API el número de fincas reales ===
  useEffect(() => {
    if (!token) {
      navigate('/login');
      return;
    }
    
    const fetchStats = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/v1/fincas/', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
          const data = await res.json();
          setFincaCount(data.length); // Contamos cuántas fincas hay
        }
      } catch (err) {
        console.error("Error al cargar estadísticas");
      }
    };
    
    fetchStats();
  }, [token, navigate]);
  // ==========================================================

  return (
    <div className="min-h-screen bg-slate-50 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-emerald-700">AgroFlow Dashboard 🌱</h1>
          <div className="flex gap-3">
            <Link 
              to="/app/fincas" 
              className="bg-emerald-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-emerald-700 transition-colors"
            >
              Ir a Fincas →
            </Link>
            <button 
              onClick={handleLogout}
              className="bg-red-500 text-white px-4 py-2 rounded-lg font-semibold hover:bg-red-600 transition-colors"
            >
              Cerrar Sesión
            </button>
          </div>
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-md border border-slate-200">
          <h2 className="text-xl font-semibold text-slate-800 mb-4">¡Bienvenido al sistema!</h2>
          <p className="text-slate-600">
            Has entrado exitosamente a AgroFlow. El backend en SQLite está corriendo perfecto y el frontend está conectado.
          </p>
          <div className="mt-6 grid grid-cols-3 gap-4">
            {/* === CONTADOR REAL DE FINCAS === */}
            <div className="bg-emerald-50 p-4 rounded-lg border border-emerald-100">
              <p className="text-sm text-emerald-600 font-medium">Fincas</p>
              <p className="text-3xl font-bold text-emerald-800">{fincaCount}</p>
            </div>
            {/* ================================ */}
            <div className="bg-amber-50 p-4 rounded-lg border border-amber-100">
              <p className="text-sm text-amber-600 font-medium">Lotes</p>
              <p className="text-3xl font-bold text-amber-800">0</p>
            </div>
            <div className="bg-sky-50 p-4 rounded-lg border border-sky-100">
              <p className="text-sm text-sky-600 font-medium">Insumos</p>
              <p className="text-3xl font-bold text-sky-800">0</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}