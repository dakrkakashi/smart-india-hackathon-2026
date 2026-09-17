import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/layout/Layout';
import Dashboard from './pages/Dashboard';
import RiskMap from './pages/RiskMap';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="map" element={<RiskMap />} />
          {/* Additional routes will be added in Phase 5 */}
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
