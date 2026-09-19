import { useNavigate } from 'react-router-dom';

export default function DashboardPage() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('agroflow_token');
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-slate-50 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-emerald-700">AgroFlow Dashboard 🌱</h1>
          <button 
            onClick={handleLogout}
            className="bg-red-500 text-white px-4 py-2 rounded-lg font-semibold hover:bg-red-600"
          >
            Cerrar Sesión
          </button>
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-md border border-slate-200">
          <h2 className="text-xl font-semibold text-slate-800 mb-4">¡Bienvenido al sistema!</h2>
          <p className="text-slate-600">
            Has entrado exitosamente a la prueba de fuego de AgroFlow. El backend en SQLite está corriendo perfecto y el frontend está conectado.
          </p>
          <div className="mt-6 grid grid-cols-3 gap-4">
            <div className="bg-emerald-50 p-4 rounded-lg">
              <p className="text-sm text-emerald-600">Fincas</p>
              <p className="text-2xl font-bold text-emerald-800">0</p>
            </div>
            <div className="bg-amber-50 p-4 rounded-lg">
              <p className="text-sm text-amber-600">Lotes</p>
              <p className="text-2xl font-bold text-amber-800">0</p>
            </div>
            <div className="bg-sky-50 p-4 rounded-lg">
              <p className="text-sm text-sky-600">Insumos</p>
              <p className="text-2xl font-bold text-sky-800">0</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}