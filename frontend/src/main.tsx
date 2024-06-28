import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { PaletteMode, createTheme } from '@mui/material';
import SignIn from './views/SignIn';
import FileManager from './views/FileManager';
import Dashboard from './views/Dashboard';
import NavigatorBar from './components/NavigatorBar';
import getCheckoutTheme from './assets/getCheckoutTheme';
import EditProfile from './views/EditProfile';

const NotFound = () => {
  return <h2>Page Not Found</h2>;
};

interface Notification {
  message: string;
  type: string;
}

const App = () => {
  const [mode, setMode] = React.useState<PaletteMode>('light');
  const [isAuthenticated, setIsAuthenticated] = React.useState(false);
  const [notiList, setNotiList] = React.useState<Notification[]>([])
  const checkoutTheme = createTheme(getCheckoutTheme(mode));

  const toggleColorMode = () => {
    setMode((prev: PaletteMode) => (prev === 'dark' ? 'light' : 'dark'));
  };

  React.useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  const handleSignOut = () => {
    // Implement sign-out logic here, e.g., clearing local storage, redirecting to login page
    localStorage.removeItem('token');
    setIsAuthenticated(false)
  };

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/file" element={
          <>
            <NavigatorBar mode={mode} toggleColorMode={toggleColorMode} theme={checkoutTheme} notiList={notiList}/>
            <FileManager theme={checkoutTheme} isAuthenticated={isAuthenticated} handleSignOut={handleSignOut} />
          </>
        }
        />
        <Route path="/login" element={<SignIn theme={checkoutTheme} setIsAuthenticated={setIsAuthenticated} />} />
        <Route path="/edit" element={
          isAuthenticated ? (
            <EditProfile theme={checkoutTheme} />
          ) : (
            <Navigate to="/login" replace />
          )} />
        <Route path="/dashboard" element={
          <>
            <NavigatorBar mode={mode} toggleColorMode={toggleColorMode} theme={checkoutTheme} notiList={notiList}/>
            <Dashboard theme={checkoutTheme} setNotiList={setNotiList}/>
          </>
        }
        />
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
