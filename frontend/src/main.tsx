import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import Dashboard from './views/Dashboard.tsx';
import NavigatorBar from './components/NavigatorBar.tsx';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { PaletteMode } from '@mui/material';
import DownloadFile from './views/DownloadFile.tsx';

const NotFound = () => {
  return <h2>Page Not Found</h2>;
};

const App = () => {
  const [mode, setMode] = React.useState<PaletteMode>('light');

  const toggleColorMode = () => {
    setMode((prev: PaletteMode) => (prev === 'dark' ? 'light' : 'dark'));
  };

  return (
    <BrowserRouter>
      <NavigatorBar mode={mode} toggleColorMode={toggleColorMode} />
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="file" element={<NotFound />} />
        <Route path="dashboard" element={<Dashboard mode={mode} />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
};

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
