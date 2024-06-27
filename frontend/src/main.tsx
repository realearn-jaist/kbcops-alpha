import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import Dashboard from './views/Dashboard.tsx';
import NavigatorBar from './components/NavigatorBar.tsx';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { PaletteMode, createTheme } from '@mui/material';
import SignIn from './views/SignIn.tsx';
import getCheckoutTheme from './assets/getCheckoutTheme.tsx';
import FileManager from './views/FileManager.tsx';

const NotFound = () => {
  return <h2>Page Not Found</h2>;
};

const App = () => {
  const [mode, setMode] = React.useState<PaletteMode>('light');
  const checkoutTheme = createTheme(getCheckoutTheme(mode));

  const toggleColorMode = () => {
    setMode((prev: PaletteMode) => (prev === 'dark' ? 'light' : 'dark'));
  };

  return (
    <BrowserRouter>
      <NavigatorBar mode={mode} toggleColorMode={toggleColorMode} theme={checkoutTheme}/>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="file" element={<FileManager theme={checkoutTheme}/>} />
        <Route path="login" element={<SignIn theme={checkoutTheme}/>} />
        <Route path="dashboard" element={<Dashboard theme={checkoutTheme} />} />
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
