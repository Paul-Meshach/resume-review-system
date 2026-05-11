import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import api from '../api/axios';

export default function ResumeUpload() {
  const [file, setFile] = useState(null);
  const [dragOver, setDragOver] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleFileChange = (selectedFile) => {
    const ext = selectedFile?.name.split('.').pop().toLowerCase();
    if (!['pdf', 'doc', 'docx'].includes(ext)) {
      toast.error('Only PDF, DOC, or DOCX files are allowed');
      return;
    }
    if (selectedFile.size > 5 * 1024 * 1024) { // 5MB limit
      toast.error('File size must be less than 5MB');
      return;
    }
    setFile(selectedFile);
  };

  const handleUpload = async () => {
    if (!file) return toast.error('Please select a file first');

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file); // 'file' must match FastAPI parameter name

    try {
      const response = await api.post('/resumes/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      toast.success('Resume uploaded and parsed successfully!');
      // Navigate to extracted details page with candidate ID
      navigate(`/extracted/${response.data.id}`);
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Upload failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold text-gray-800 mb-2">Upload Resume</h1>
      <p className="text-gray-500 mb-6">Upload a candidate resume to extract details automatically</p>

      {/* Drag and Drop Zone */}
      <div
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDragOver(false);
          handleFileChange(e.dataTransfer.files[0]);
        }}
        onClick={() => document.getElementById('fileInput').click()}
        className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition
          ${dragOver ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'}`}
      >
        <input
          id="fileInput"
          type="file"
          accept=".pdf,.doc,.docx"
          className="hidden"
          onChange={(e) => handleFileChange(e.target.files[0])}
        />

        {file ? (
          <div>
            <div className="text-4xl mb-3">📄</div>
            <p className="font-semibold text-gray-700">{file.name}</p>
            <p className="text-sm text-gray-400 mt-1">
              {(file.size / 1024).toFixed(1)} KB — Click to change
            </p>
          </div>
        ) : (
          <div>
            <div className="text-5xl mb-4">☁️</div>
            <p className="text-lg font-medium text-gray-600">
              Drag & drop or click to upload
            </p>
            <p className="text-sm text-gray-400 mt-2">PDF, DOC, DOCX up to 5MB</p>
          </div>
        )}
      </div>

      <button
        onClick={handleUpload}
        disabled={!file || loading}
        className="mt-6 w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300
                   text-white font-semibold py-3 rounded-lg transition"
      >
        {loading ? (
          <span className="flex items-center justify-center gap-2">
            <span className="animate-spin h-4 w-4 border-2 border-white
                             border-t-transparent rounded-full" />
            Parsing Resume... (this may take a moment)
          </span>
        ) : '🚀 Upload & Extract'}
      </button>
    </div>
  );
}