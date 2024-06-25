import * as React from 'react';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import { Container } from '@mui/material';
import MyAppBar from '../components/MyAppBar';
import FileList from '../components/DownloadFileComponents/FileList';

// Define the theme for the app
const defaultTheme = createTheme();

export default function App() {
  // State variables for controlling drawer open state
  const [open, setOpen] = React.useState(true);

  // Toggle the drawer open/close state
  const toggleDrawer = () => {
    setOpen(!open);
  };

  return (
    <ThemeProvider theme={defaultTheme}>
      <CssBaseline />
      <Box sx={{ display: 'flex' }}>
        <MyAppBar open={false} toggleDrawer={toggleDrawer} openable={false}/>
        <Box
          component="main"
          sx={{
            backgroundColor: (theme) =>
              theme.palette.mode === 'light'
                ? theme.palette.grey[100]
                : theme.palette.grey[900],
            flexGrow: 1,
            height: '100vh',
            overflow: 'auto',
          }}
        >
          <Toolbar />
          <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            <h1>File Manager</h1>
            <FileList />
          </Container>
        </Box>
      </Box>
    </ThemeProvider>
  );
}
