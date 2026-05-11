// This page is accessed by TL via email link — NO login required
// Token from URL query param is the only authentication

import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { toast } from 'react-toastify';
import api from '../api/axios';

export default function TLReview() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');

  const [reviewData, setReviewData] = useState(null);
  const [status, setStatus] = useState('');
  const [comments, setComments] = useState('');
  const [loading, setLoading] = useState(true);
  const [submitted, setSubmitted] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!token) {
      setError('Invalid review link — no token found');
      setLoading(false);
      return;
    }
    api.get(`/reviews/by-token/${token}`)
      .then(res => setReviewData(res.data))
      .catch(err => setError(err.response?.data?.detail || 'Invalid or expired link'))
      .finally(() => setLoading(false));
  }, [token]);

  const handleSubmit = async () => {
    if (!status) return toast.error('Please select Shortlisted or Not Shortlisted');

    setSubmitting(true);
    try {
      await api.post('/reviews/submit', { token, status, comments });
      setSubmitted(true);
      toast.success('Review submitted successfully!');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Submission failed');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return (
    <div className="flex justify-center items-center h-screen">
      <div className="animate-spin h-12 w-12 border-4 border-blue-600
                      border-t-transparent rounded-full" />
    </div>
  );

  if (error) return (
    <div className="flex items-center justify-center h-screen">
      <div className="text-center max-w-sm">
        <div className="text-5xl mb-4">🔗</div>
        <h2 className="text-xl font-bold text-gray-800 mb-2">Link Issue</h2>
        <p className="text-red-500">{error}</p>
      </div>
    </div>
  );

  if (submitted) return (
    <div className="flex items-center justify-center h-screen">
      <div className="text-center max-w-sm">
        <div className="text-6xl mb-4">✅</div>
        <h2 className="text-2xl font-bold text-gray-800 mb-2">Review Submitted!</h2>
        <p className="text-gray-500">
          The admin has been notified of your decision. Thank you!
        </p>
      </div>
    </div>
  );

  const c = reviewData?.candidate;

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-2xl mx-auto">
        <div className="bg-white rounded-2xl shadow-sm border p-6 mb-6">
          <h1 className="text-2xl font-bold text-gray-800 mb-1">Resume Review</h1>
          <p className="text-gray-500">Assigned by Admin • Please review and submit your decision</p>
        </div>

        {/* Candidate Details */}
        <div className="bg-white rounded-2xl shadow-sm border p-6 mb-6">
          <h2 className="font-semibold text-gray-700 mb-4 text-lg">Candidate Profile</h2>
          <div className="grid grid-cols-2 gap-4">
            {[
              ['Name', c?.name], ['Email', c?.email],
              ['Phone', c?.phone], ['Qualification', c?.qualification],
              ['Experience', c?.years_of_experience], ['Domain', c?.domain],
            ].map(([label, value]) => (
              <div key={label}>
                <p className="text-xs text-gray-400 uppercase font-medium">{label}</p>
                <p className="font-medium text-gray-800">{value || '—'}</p>
              </div>
            ))}
          </div>
          {c?.skills && (
            <div className="mt-4">
              <p className="text-xs text-gray-400 uppercase font-medium mb-2">Skills</p>
              <div className="flex flex-wrap gap-2">
                {c.skills.split(',').map(skill => (
                  <span key={skill} className="bg-blue-50 text-blue-700 text-sm
                                               px-3 py-1 rounded-full font-medium">
                    {skill.trim()}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Decision */}
        <div className="bg-white rounded-2xl shadow-sm border p-6 mb-6">
          <h2 className="font-semibold text-gray-700 mb-4 text-lg">Your Decision</h2>
          <div className="flex gap-4 mb-4">
            <button
              onClick={() => setStatus('shortlisted')}
              className={`flex-1 py-4 rounded-xl font-semibold border-2 transition
                ${status === 'shortlisted'
                  ? 'border-green-500 bg-green-50 text-green-700'
                  : 'border-gray-200 text-gray-500 hover:border-green-300'}`}
            >
              ✅ Shortlisted
            </button>
            <button
              onClick={() => setStatus('rejected')}
              className={`flex-1 py-4 rounded-xl font-semibold border-2 transition
                ${status === 'rejected'
                  ? 'border-red-500 bg-red-50 text-red-700'
                  : 'border-gray-200 text-gray-500 hover:border-red-300'}`}
            >
              ❌ Not Shortlisted
            </button>
          </div>

          <textarea
            value={comments}
            onChange={(e) => setComments(e.target.value)}
            placeholder="Add comments (optional) — feedback for the candidate..."
            className="w-full p-3 border border-gray-300 rounded-lg text-sm
                       focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
            rows={3}
          />

          <button
            onClick={handleSubmit}
            disabled={!status || submitting}
            className="mt-4 w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300
                       text-white font-semibold py-3 rounded-lg transition"
          >
            {submitting ? 'Submitting...' : 'Submit Review Decision'}
          </button>
        </div>
      </div>
    </div>
  );
}