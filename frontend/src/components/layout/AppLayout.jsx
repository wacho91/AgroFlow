import { Outlet, NavLink, useNavigate } from 'react-router-dom';

export default function AppLayout() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('agroflow_token');
    navigate('/login');
  };

  // Clases unificadas para los botones del menú
  const linkClass = ({ isActive }) =>
    `flex items-center gap-3 px-4 py-3 rounded-lg font-medium transition-colors ${
      isActive 
        ? 'bg-emerald-600 text-white shadow-lg' 
        : 'text-slate-300 hover:bg-slate-800 hover:text-white'
    }`;

  return (
    <div className="min-h-screen bg-slate-100 flex">
      {/* === SIDEBAR (Menú Lateral) === */}
      <aside className="w-64 bg-slate-900 text-white flex flex-col p-4 fixed h-full">
        <div className="mb-8 px-4 py-4">
          <h1 className="text-2xl font-bold text-emerald-400">AgroFlow 🌱</h1>
        </div>
        <nav className="flex-1 space-y-2">
          <NavLink to="/app" end className={linkClass}>
            <span>📊</span> Dashboard
          </NavLink>
          <NavLink to="/app/fincas" className={linkClass}>
            <span>🏡</span> Fincas
          </NavLink>
          <NavLink to="/app/lotes" className={linkClass}>
            <span>🗺️</span> Lotes
          </NavLink>
          <NavLink to="/app/insumos" className={linkClass}>
            <span>🧪</span> Insumos
          </NavLink>
          <NavLink to="/app/cultivos" className={linkClass}>
            <span>🌿</span> Cultivos
          </NavLink>
          <NavLink to="/app/jornaleros" className={linkClass}>
            <span>👷‍♂️</span> Jornaleros
          </NavLink>
          <NavLink to="/app/tesoreria" className={linkClass}>
            <span>💰</span> Tesorería
          </NavLink>
          <NavLink to="/app/eventos" className={linkClass}>
            <span>⚡</span> Eventos
          </NavLink>
        </nav>
        <div className="mt-auto">
          <button 
            onClick={handleLogout}
            className="w-full flex items-center gap-3 px-4 py-3 rounded-lg font-medium text-red-400 hover:bg-red-900/50 transition-colors"
          >
            <span>🚪</span> Cerrar Sesión
          </button>
        </div>
      </aside>

      {/* === CONTENIDO PRINCIPAL === */}
      <main className="flex-1 ml-64 p-8 overflow-y-auto">
        <Outlet /> {/* Aquí se renderizarán las páginas */}
      </main>
    </div>
  );
}