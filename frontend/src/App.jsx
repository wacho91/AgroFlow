import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import AppLayout from './components/layout/AppLayout';
import DashboardPage from './pages/DashboardPage';
import FincasPage from './pages/FincasPage';
import LotesPage from './pages/LotesPage';
import InsumosPage from './pages/InsumosPage';
import CultivosPage from './pages/CultivosPage';
import TesoreriaPage from './pages/TesoreriaPage';
import EventosPage from './pages/EventosPage';
import JornalerosPage from './pages/JornalerosPage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        
        {/* Todo lo que esté dentro de /app usará el AppLayout (Sidebar) */}
        <Route path="/app" element={<AppLayout />}>
          <Route index element={<DashboardPage />} />
          <Route path="fincas" element={<FincasPage />} />
          <Route path="lotes" element={<LotesPage />} />
          <Route path="insumos" element={<InsumosPage />} />
          <Route path="cultivos" element={<CultivosPage />} />
          <Route path="tesoreria" element={<TesoreriaPage />} />
          <Route path="jornaleros" element={<JornalerosPage />} />
          <Route path="eventos" element={<EventosPage />} />
        </Route>
        
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </BrowserRouter>
  );
}