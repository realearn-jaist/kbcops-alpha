import React, { useState } from 'react';
import { AppBar as MuiAppBar, Toolbar, IconButton, Tabs, Tab, TextField, Popover, List, ListItem, ListItemText, Box, AppBar, PaletteMode, Theme, ThemeProvider } from '@mui/material';
import { styled } from '@mui/material/styles';
import MenuIcon from '@mui/icons-material/Menu';
import NotificationsIcon from '@mui/icons-material/Notifications';
import { useLocation, useNavigate } from 'react-router-dom';
import ToggleColorMode from './displayDashboardComponents/ToggleColorMode';

interface NavigatorBarProps {
  mode: PaletteMode
  toggleColorMode: () => void;
  theme: Theme
}


// Functional component for the AppBar
const NavigatorBar = ({ mode, toggleColorMode, theme }: NavigatorBarProps) => {
  const location = useLocation();
  const navigate = useNavigate();

  // Define the paths for the tabs
  const pages = [
    { label: 'Dashboard', path: '/dashboard' },
    { label: 'File', path: '/file' }
  ];

  const currentPath = location.pathname;

  const handleTabChange = (event: React.SyntheticEvent, newValue: string) => {
    navigate(newValue);
  };

  // State for notification popover
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  const handleNotificationClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleNotificationClose = () => {
    setAnchorEl(null);
  };

  const openPopover = Boolean(anchorEl);
  const popoverId = openPopover ? 'notification-popover' : undefined;

  // Dummy notifications data
  const notifications = [
    "Notification 1",
    "Notification 2",
    "Notification 3"
  ];

  return (
    <ThemeProvider theme={theme}>
      <AppBar position="fixed" sx={{ boxShadow: 'true' }}>
        <Toolbar sx={{ minHeight: 48, padding: '0 !important', paddingRight: 1, height: "100%" }}>
          {/* Menu button to toggle the drawer */}

          {/* Navigation tabs */}
          <Tabs
            value={currentPath}
            onChange={handleTabChange}
            indicatorColor="primary"
            textColor="inherit"
            sx={{
              flexGrow: 1,
              minHeight: 48,
              '& .MuiTabs-flexContainer': {
                height: '100%',
              },
              '& .MuiTab-root': {
                minHeight: 48,
                height: '100%', // Ensure the tab takes the full height
                minWidth: 100, // Minimum width for tabs
                color: 'grey', // Default text color
                textTransform: 'none', // Prevent uppercase
                padding: 0, // Remove padding from tabs
                display: 'flex', // Use flex display
                alignItems: 'center', // Center items vertically
                '&.Mui-selected': {
                  color: 'white', // Selected tab text color
                  backgroundColor: 'grey', // Selected tab background color
                },
                '&:hover': {
                  backgroundColor: 'lightgrey', // Hover effect
                },
                '&:not(:last-of-type)': {
                  borderRight: '1px solid grey', // Separator line
                },
              },
            }}
          >
            {pages.map((page) => (
              <Tab
                key={page.path}
                label={page.label}
                value={page.path}
              />
            ))}
          </Tabs>

          {/* Secret Key text fields */}
          {/* <TextField
          variant="outlined"
          size="small"
          placeholder="Secret Key"
          sx={{ marginRight: 2, backgroundColor: 'white' }}
        /> */}

          {/* Notification button */}
          <IconButton onClick={handleNotificationClick} sx={{ marginRight: '10px' }}>
            <NotificationsIcon />
          </IconButton>
          <Popover
            id={popoverId}
            open={openPopover}
            anchorEl={anchorEl}
            onClose={handleNotificationClose}
            anchorOrigin={{
              vertical: 'bottom',
              horizontal: 'right',
            }}
            transformOrigin={{
              vertical: 'top',
              horizontal: 'right',
            }}
          >
            <List>
              {notifications.map((notification, index) => (
                <ListItem key={index}>
                  <ListItemText primary={notification} />
                </ListItem>
              ))}
            </List>
          </Popover>

          <ToggleColorMode mode={mode} toggleColorMode={toggleColorMode} />
        </Toolbar>
      </AppBar>
    </ThemeProvider>

  );
};

export default NavigatorBar;