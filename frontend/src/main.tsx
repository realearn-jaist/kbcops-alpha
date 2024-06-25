import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Dashboard from './views/Dashboard.tsx';
import './index.css';
import SignIn from './views/SignIn.tsx';
import SignUp from './views/SignUp.tsx';
import DownloadFile from './views/DownloadFile.tsx';

// Optional NotFound Component
const NotFound = () => {
  return <h2>Page Not Found</h2>;
};

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="file" element={<DownloadFile />} />
        <Route path="dashboard" element={<Dashboard />} />
        {/* Optional: Add a NotFound Route */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>,
);
