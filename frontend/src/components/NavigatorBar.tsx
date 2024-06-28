import React, { useState } from 'react';
import { Toolbar, IconButton, Tabs, Tab, Popover, List, ListItem, ListItemText, AppBar, PaletteMode, Theme, ThemeProvider } from '@mui/material';
import NotificationsIcon from '@mui/icons-material/Notifications';
import { useLocation, useNavigate } from 'react-router-dom';
import ToggleColorMode from './displayDashboardComponents/ToggleColorMode';
import { Info, CheckCircle, Error } from '@mui/icons-material';

interface Notification {
  message: string;
  type: string;
}

interface NavigatorBarProps {
  mode: PaletteMode;
  toggleColorMode: () => void;
  theme: Theme;
  notiList: Notification[];
}

// Functional component for the AppBar
const NavigatorBar = ({ mode, toggleColorMode, theme, notiList }: NavigatorBarProps) => {
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

  const getIcon = (type: string) => {
    switch (type) {
      case 'info':
        return <Info />;
      case 'success':
        return <CheckCircle />;
      case 'error':
        return <Error />;
      default:
        return null;
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <AppBar position="fixed" sx={{ boxShadow: 'true' }}>
        <Toolbar sx={{ minHeight: 48, padding: '0 !important', paddingRight: 1, height: "100%" }}>
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

          {/* Notification button */}
          <IconButton onClick={handleNotificationClick} sx={{ marginRight: '10px' }}>
            <NotificationsIcon />
          </IconButton>

          {/* Notification Popover */}
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
              {notiList.map((notification, index) => (
                <ListItem key={index}>
                  {/* Render icon based on notification type */}
                  {getIcon(notification.type)}
                  <ListItemText sx={{marginLeft: 1}}
                    primary={notification.message}
                    primaryTypographyProps={{
                      color: notification.type === 'error' ? 'error' : 'primary',
                    }}
                  />
                </ListItem>
              ))}
            </List>
          </Popover>

          {/* Toggle color mode button */}
          <ToggleColorMode mode={mode} toggleColorMode={toggleColorMode} />
        </Toolbar>
      </AppBar>
    </ThemeProvider>
  );
};

export default NavigatorBar;