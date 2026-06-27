import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AppShell } from './components/layout/AppShell.jsx';
import DashboardPage from './pages/DashboardPage.jsx';
import AssistantPage from './pages/AssistantPage.jsx';
import LiveCallPage from './pages/LiveCallPage.jsx';

export default function App() {
  return (
    <BrowserRouter>
      <AppShell>
        <Routes>
          <Route path="/"           element={<DashboardPage />} />
          <Route path="/assistant"  element={<AssistantPage />} />
          <Route path="/live-call"  element={<LiveCallPage />} />
        </Routes>
      </AppShell>
    </BrowserRouter>
  );
}