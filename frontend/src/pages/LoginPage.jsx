import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      // Hacemos la petición real a nuestro backend en FastAPI
      const response = await fetch('http://localhost:8000/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      
      const data = await response.json();
      
      // Si el backend responde con un error (ej: contraseña incorrecta)
      if (!response.ok) {
        throw new Error(data.detail || 'Error al iniciar sesión');
      }
      
      // Guardamos el token real que nos dio FastAPI
      localStorage.setItem('agroflow_token', data.access_token);
      // ¡Lo mandamos al dashboard!
      navigate('/app'); 
      
    } catch (err) {
      alert(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen flex items-center justify-center px-4 py-12 overflow-hidden">
      
      {/* === FONDO DE CAMPO AGRÍCOLA DIFUMINADO === */}
      <div 
        className="absolute inset-0 z-0 bg-cover bg-center" 
        style={{ backgroundImage: "url('https://images.unsplash.com/photo-1500382017468-9049fed747ef?q=80&w=2070&auto=format&fit=crop')" }}
      ></div>
      
      {/* Capa oscura difuminada para dar contraste */}
      <div className="absolute inset-0 z-0 bg-gradient-to-t from-slate-900 via-slate-900/70 to-slate-900/50 backdrop-blur-md"></div>
      
      {/* Marca de agua gigante con el nombre de la empresa */}
      <div className="absolute inset-0 z-0 flex items-center justify-center pointer-events-none">
        <h1 className="text-[18vw] font-extrabold text-white/5 tracking-tighter select-none">
          AgroFlow
        </h1>
      </div>

      {/* Tarjeta de Login translúcida (Glassmorphism) */}
      <div className="relative z-10 max-w-md w-full bg-white/10 dark:bg-gray-800/30 backdrop-blur-xl p-8 rounded-2xl shadow-2xl border border-white/20">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-extrabold text-white drop-shadow-lg">AgroFlow</h1>
          <p className="text-emerald-300 mt-2 text-sm font-medium tracking-wide">SISTEMA DE GESTIÓN AGRÍCOLA</p>
        </div>
        
        <form onSubmit={handleLogin} className="space-y-6">
          <div>
            <label className="block text-sm font-semibold text-emerald-100 mb-2">Correo electrónico</label>
            <input 
              type="email" 
              required 
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-300 focus:ring-2 focus:ring-emerald-400 focus:border-transparent focus:outline-none backdrop-blur-sm"
              placeholder="admin@agroflow.com"
            />
          </div>
          
          <div>
            <label className="block text-sm font-semibold text-emerald-100 mb-2">Contraseña</label>
            <input 
              type="password" 
              required 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-300 focus:ring-2 focus:ring-emerald-400 focus:border-transparent focus:outline-none backdrop-blur-sm"
              placeholder="********"
            />
          </div>

          <button 
            type="submit" 
            disabled={loading}
            className="w-full bg-gradient-to-r from-emerald-600 to-teal-500 text-white font-bold py-3 rounded-lg shadow-lg hover:shadow-emerald-500/30 hover:scale-[1.02] transition-all disabled:opacity-50"
          >
            {loading ? 'Verificando...' : 'Iniciar Sesión'}
          </button>
        </form>
      </div>
    </div>
  );
}