import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/layout/Layout';
import Dashboard from './pages/Dashboard';
import RiskMap from './pages/RiskMap';
import Sensors from './pages/Sensors';
import Alerts from './pages/Alerts';
import Regions from './pages/Regions';
import { ErrorBoundary } from './components/ErrorBoundary';

function App() {
  return (
    <ErrorBoundary>
      <Router>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Dashboard />} />
            <Route path="map" element={<RiskMap />} />
            <Route path="sensors" element={<Sensors />} />
            <Route path="alerts" element={<Alerts />} />
            <Route path="regions" element={<Regions />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Routes>
      </Router>
    </ErrorBoundary>
  );
}

export default App;
