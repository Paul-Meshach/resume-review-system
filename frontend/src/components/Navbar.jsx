import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useEffect, useState } from 'react';
import api from '../api/axios';

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
    if (user?.role === 'admin') {
      api.get('/notifications/unread-count')
        .then(res => setUnreadCount(res.data.count))
        .catch(() => {});
    }
  }, [location, user]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navLink = (to, label) => (
    <Link to={to}
      className={`text-sm font-medium transition px-3 py-2 rounded-lg
        ${location.pathname.startsWith(to)
          ? 'bg-blue-100 text-blue-700'
          : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'}`}>
      {label}
    </Link>
  );

  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link to="/dashboard" className="font-bold text-blue-700 text-lg">
          📋 ResumeReview
        </Link>

        {user && (
          <div className="flex items-center gap-2">
            {navLink('/upload', '⬆️ Upload')}
            <Link to="/notifications"
              className={`relative text-sm font-medium px-3 py-2 rounded-lg transition
                ${location.pathname === '/notifications'
                  ? 'bg-blue-100 text-blue-700'
                  : 'text-gray-600 hover:bg-gray-100'}`}>
              🔔 Alerts
              {unreadCount > 0 && (
                <span className="absolute -top-1 -right-1 bg-red-500 text-white
                                 text-xs w-5 h-5 rounded-full flex items-center justify-center">
                  {unreadCount}
                </span>
              )}
            </Link>
            <div className="ml-4 flex items-center gap-3 pl-4 border-l border-gray-200">
              <span className="text-sm text-gray-600">
                {user.name} <span className="text-xs bg-gray-100 px-2 py-0.5 rounded">{user.role}</span>
              </span>
              <button onClick={handleLogout}
                className="text-sm text-red-500 hover:text-red-700 font-medium transition">
                Logout
              </button>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}