import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { ThemeProvider, Theme } from '@mui/material/styles';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

export default function EditProfile({ theme }: { theme: Theme }) {
  const navigate = useNavigate();
  const BACKEND_URI = import.meta.env.VITE_BACKEND_URI || "http://127.0.0.1:5000";
  const [error, setError] = React.useState<string>('');
  const [username, setUsername] = React.useState<string>(''); // State to hold username

  React.useEffect(() => {
    // Fetch the current username when component mounts
    axios.get(`${BACKEND_URI}/api/auth/username`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}` // Include JWT token for authentication
      }
    })
      .then(response => {
        setUsername(response.data.username); // Set the username in state
      })
      .catch(error => {
        console.error('Failed to fetch username:', error);
        // Handle error if needed
      });
  }, []); // Empty dependency array ensures this effect runs only once on mount

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const token = localStorage.getItem('token');
    const data = new FormData(event.currentTarget);
    const username = data.get('username');
    const password = data.get('password');
    const newPassword = data.get('newPassword');

    axios.post(`${BACKEND_URI}/api/auth/update`, { username, password, newPassword }, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      .then(response => {
        console.log("Change credentials successfully:", response.data);
        // Handle success if needed
        navigate('/'); // Navigate to home or appropriate page after changing credentials
      })
      .catch(error => {
        console.error("Change credentials failed:", error);
        if (error.response && error.response.status === 401) {
          setError('Invalid credentials');
        } else {
          setError('Failed to change credentials. Please try again.');
        }
      });
  };

  const handleUsernameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setUsername(event.target.value); // Update username state on input change
  };

  return (
    <ThemeProvider theme={theme}>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Change Username & Password
          </Typography>
          {error && (
            <Typography variant="body2" color="error" align="center" sx={{ mt: 1 }}>
              {error}
            </Typography>
          )}
          <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="username"
              label="Current Username"
              name="username"
              autoFocus
              value={username} // Bind username state to input value
              onChange={handleUsernameChange} // Handle input change
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Current Password"
              type="password"
              id="password"
              autoComplete="current-password"
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="newPassword"
              label="New Password"
              type="password"
              id="newPassword"
              autoComplete="new-password"
            />

            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Change Credentials
            </Button>
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
}
