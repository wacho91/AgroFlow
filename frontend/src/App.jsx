import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import FincasPage from './pages/FincasPage';
import LotesPage from './pages/LotesPage';
import InsumosPage from './pages/InsumosPage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/app" element={<DashboardPage />} />
        <Route path="/app/fincas" element={<FincasPage />} />
        <Route path="/app/lotes" element={<LotesPage />} />
        <Route path="/app/insumos" element={<InsumosPage />} />
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </BrowserRouter>
  );
}