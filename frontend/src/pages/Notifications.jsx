import { useEffect, useState } from 'react';
import { toast } from 'react-toastify';
import api from '../api/axios';

export default function Notifications() {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchNotifications = () => {
    api.get('/notifications/')
      .then(res => setNotifications(res.data))
      .catch(() => toast.error('Failed to load notifications'))
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchNotifications(); }, []);

  const markAsRead = async (id) => {
    await api.patch(`/notifications/${id}/read`);
    setNotifications(prev =>
      prev.map(n => n.id === id ? { ...n, is_read: true } : n)
    );
  };

  const unread = notifications.filter(n => !n.is_read).length;

  if (loading) return (
    <div className="flex justify-center items-center h-64">
      <div className="animate-spin h-10 w-10 border-4 border-blue-600
                      border-t-transparent rounded-full" />
    </div>
  );

  return (
    <div className="max-w-2xl mx-auto p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">Notifications</h1>
          <p className="text-gray-500">{unread} unread</p>
        </div>
        <button onClick={fetchNotifications}
          className="text-sm text-blue-600 hover:underline">
          🔄 Refresh
        </button>
      </div>

      {notifications.length === 0 ? (
        <div className="text-center py-16 text-gray-400">
          <div className="text-5xl mb-4">🔔</div>
          <p>No notifications yet. They'll appear here after TLs submit reviews.</p>
        </div>
      ) : (
        <div className="space-y-3">
          {notifications.map((n) => (
            <div
              key={n.id}
              onClick={() => !n.is_read && markAsRead(n.id)}
              className={`p-4 rounded-xl border cursor-pointer transition
                ${n.is_read
                  ? 'bg-white border-gray-200 opacity-60'
                  : 'bg-blue-50 border-blue-200 shadow-sm'}`}
            >
              <div className="flex items-start gap-3">
                <span className="text-2xl mt-0.5">
                  {n.message.includes('Shortlisted') ? '✅' : '❌'}
                </span>
                <div className="flex-1">
                  <p className={`text-gray-800 ${!n.is_read ? 'font-semibold' : ''}`}>
                    {n.message}
                  </p>
                  <p className="text-xs text-gray-400 mt-1">
                    {new Date(n.created_at).toLocaleString()}
                  </p>
                </div>
                {!n.is_read && (
                  <span className="w-2.5 h-2.5 bg-blue-500 rounded-full mt-1.5 flex-shrink-0" />
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}