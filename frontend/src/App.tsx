import { Routes, Route, Navigate } from 'react-router-dom';
import NewResearchPage from './pages/research/NewResearchPage';
import ResearchDetailPage from './pages/research/ResearchDetailPage';
import ResearchReviewPage from './pages/research/ResearchReviewPage';
import ReportPage from './pages/research/ReportPage';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/research/new" replace />} />
      <Route path="/research/new" element={<NewResearchPage />} />
      <Route path="/research/:runId" element={<ResearchDetailPage />} />
      <Route path="/research/:runId/review" element={<ResearchReviewPage />} />
      <Route path="/research/:runId/report" element={<ReportPage />} />
    </Routes>
  );
}

export default App;
