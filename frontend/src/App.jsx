import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Navbar from './components/Navbar';
import Login from './pages/Login';
import ResumeUpload from './pages/ResumeUpload';
import ExtractedDetails from './pages/ExtractedDetails';
import TLSelection from './pages/TLSelection';
import TLReview from './pages/TLReview';
import Notifications from './pages/Notifications';

// Simple Dashboard
function Dashboard() {
  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {[
          { title: 'Upload Resume', desc: 'Upload and parse a new candidate resume',
            link: '/upload', icon: '⬆️' },
          { title: 'Notifications', desc: 'View TL review decisions',
            link: '/notifications', icon: '🔔' },
        ].map(card => (
          <a key={card.title} href={card.link}
            className="block bg-white p-6 rounded-xl border border-gray-200
                       hover:shadow-md hover:border-blue-300 transition">
            <div className="text-3xl mb-3">{card.icon}</div>
            <h3 className="font-semibold text-gray-800 mb-1">{card.title}</h3>
            <p className="text-sm text-gray-500">{card.desc}</p>
          </a>
        ))}
      </div>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <div className="min-h-screen bg-gray-50">
          <Navbar />
          <Routes>
            {/* Public routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/tl-review" element={<TLReview />} />

            {/* Protected routes (admin only) */}
            <Route path="/dashboard" element={
              <ProtectedRoute><Dashboard /></ProtectedRoute>
            } />
            <Route path="/upload" element={
              <ProtectedRoute><ResumeUpload /></ProtectedRoute>
            } />
            <Route path="/extracted/:id" element={
              <ProtectedRoute><ExtractedDetails /></ProtectedRoute>
            } />
            <Route path="/tl-select/:candidateId" element={
              <ProtectedRoute><TLSelection /></ProtectedRoute>
            } />
            <Route path="/notifications" element={
              <ProtectedRoute><Notifications /></ProtectedRoute>
            } />

            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </div>
        <ToastContainer position="top-right" autoClose={3000} />
      </BrowserRouter>
    </AuthProvider>
  );
}