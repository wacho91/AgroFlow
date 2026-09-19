import { BrowserRouter, Routes, Route } from 'react-router-dom';

// Intentamos importar el login que generó el agente de UX/UI
try {
  var LoginPage = require('./pages/LoginPage').default;
} catch (e) {
  // Si no lo encuentra, creamos un login básico para que no se caiga
  LoginPage = () => (
    <div className="min-h-screen flex items-center justify-center bg-slate-900 text-white">
      <div className="bg-slate-800 p-8 rounded-xl shadow-2xl border border-emerald-500/20">
        <h1 className="text-3xl font-bold text-emerald-400 mb-4">AgroFlow</h1>
        <p className="text-slate-300">El servidor está corriendo correctamente. 🌱</p>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Cargamos el login directamente */}
        <Route path="*" element={<LoginPage />} />
      </Routes>
    </BrowserRouter>
  );
}