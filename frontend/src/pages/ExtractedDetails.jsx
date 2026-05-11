import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import api from '../api/axios';

const Field = ({ label, value }) => (
  <div className="bg-gray-50 rounded-lg p-4">
    <p className="text-xs font-medium text-gray-400 uppercase tracking-wide mb-1">{label}</p>
    <p className="text-gray-800 font-medium">{value ||
      <span className="text-gray-400 italic">Not detected</span>}
    </p>
  </div>
);

export default function ExtractedDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [candidate, setCandidate] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get(`/resumes/${id}`)
      .then(res => setCandidate(res.data))
      .catch(() => toast.error('Failed to load candidate data'))
      .finally(() => setLoading(false));
  }, [id]);

  const handleDownload = () => {
    window.open(`http://localhost:8000/resumes/${id}/download`, '_blank');
  };

  if (loading) return (
    <div className="flex justify-center items-center h-64">
      <div className="animate-spin h-10 w-10 border-4 border-blue-600
                      border-t-transparent rounded-full" />
    </div>
  );

  if (!candidate) return <div className="p-6 text-red-500">Candidate not found</div>;

  return (
    <div className="max-w-3xl mx-auto p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">Extracted Details</h1>
          <p className="text-gray-500">Review and verify the parsed resume data</p>
        </div>
        <button
          onClick={handleDownload}
          className="flex items-center gap-2 px-4 py-2 border border-gray-300
                     rounded-lg hover:bg-gray-50 text-sm font-medium transition"
        >
          📥 Download Resume
        </button>
      </div>

      <div className="bg-white rounded-xl shadow-sm border p-6 mb-6">
        <h2 className="font-semibold text-gray-700 mb-4">Candidate Information</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Field label="Full Name" value={candidate.name} />
          <Field label="Email" value={candidate.email} />
          <Field label="Phone" value={candidate.phone} />
          <Field label="Qualification" value={candidate.qualification} />
          <Field label="Years of Experience" value={candidate.years_of_experience} />
          <Field label="Domain" value={candidate.domain} />
        </div>
        <div className="mt-4">
          <Field label="Skills" value={candidate.skills} />
        </div>
      </div>

      <div className="flex gap-3">
        <button
          onClick={() => navigate('/upload')}
          className="flex-1 border border-gray-300 text-gray-600 py-3 rounded-lg
                     hover:bg-gray-50 font-medium transition"
        >
          ← Upload Another
        </button>
        <button
          onClick={() => navigate(`/tl-select/${id}`)}
          className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-3
                     rounded-lg font-medium transition"
        >
          Assign to Team Lead →
        </button>
      </div>
    </div>
  );
}