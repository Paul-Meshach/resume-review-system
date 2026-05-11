import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import api from '../api/axios';

export default function TLSelection() {
  const { candidateId } = useParams();
  const navigate = useNavigate();
  const [tls, setTls] = useState([]);
  const [selectedTL, setSelectedTL] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.get('/tls/')
      .then(res => setTls(res.data))
      .catch(() => toast.error('Failed to load team leads'));
  }, []);

  const handleSendForReview = async () => {
    if (!selectedTL) return toast.error('Please select a Team Lead');

    setLoading(true);
    try {
      await api.post('/reviews/send', {
        candidate_id: parseInt(candidateId),
        tl_id: selectedTL,
      });
      toast.success('Resume sent for review! TL will receive an email.');
      navigate('/dashboard');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to send for review');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold text-gray-800 mb-2">Select Team Lead</h1>
      <p className="text-gray-500 mb-6">Choose a TL to review this candidate's resume</p>

      <div className="space-y-3 mb-8">
        {tls.length === 0 && (
          <p className="text-center text-gray-400 py-8">No Team Leads available</p>
        )}
        {tls.map((tl) => (
          <label
            key={tl.id}
            className={`flex items-center gap-4 p-4 rounded-xl border-2 cursor-pointer transition
              ${selectedTL === tl.id
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-200 hover:border-gray-300 bg-white'}`}
          >
            <input
              type="radio"
              name="tl"
              value={tl.id}
              checked={selectedTL === tl.id}
              onChange={() => setSelectedTL(tl.id)}
              className="accent-blue-600 w-4 h-4"
            />
            {/* Avatar circle with initials */}
            <div className="w-10 h-10 bg-indigo-100 text-indigo-700 rounded-full
                            flex items-center justify-center font-bold text-sm">
              {tl.name.split(' ').map(n => n[0]).join('')}
            </div>
            <div>
              <p className="font-semibold text-gray-800">{tl.name}</p>
              <p className="text-sm text-gray-400">{tl.email}</p>
            </div>
            {selectedTL === tl.id && (
              <span className="ml-auto text-blue-500 font-medium text-sm">Selected ✓</span>
            )}
          </label>
        ))}
      </div>

      <button
        onClick={handleSendForReview}
        disabled={!selectedTL || loading}
        className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300
                   text-white font-semibold py-3 rounded-lg transition"
      >
        {loading ? 'Sending...' : '📧 Send for Review'}
      </button>
    </div>
  );
}
