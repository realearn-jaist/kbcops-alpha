import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import Dashboard from './views/Dashboard.tsx'
import NavigatorBar from './components/NavigatorBar.tsx'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'

const NotFound = () => {
  return <h2>Page Not Found</h2>;
};

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>

    <BrowserRouter>
      <NavigatorBar />
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="file" element={<NotFound />} />
        <Route path="dashboard" element={<Dashboard />} />
        {/* Optional: Add a NotFound Route */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>,
)
