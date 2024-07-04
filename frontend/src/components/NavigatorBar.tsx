import React, { useState, useEffect } from 'react';
import { Toolbar, IconButton, Tabs, Tab, Popover, List, ListItem, ListItemText, AppBar, PaletteMode, Theme, ThemeProvider, Badge, TextField } from '@mui/material';
import NotificationsIcon from '@mui/icons-material/Notifications';
import { useLocation, useNavigate } from 'react-router-dom';
import ToggleColorMode from './displayDashboardComponents/ToggleColorMode';
import { CheckCircle, Error, Pending } from '@mui/icons-material';

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

const NavigatorBar = ({ mode, toggleColorMode, theme, notiList }: NavigatorBarProps) => {
  const location = useLocation();
  const navigate = useNavigate();

  const pages = [
    { label: 'Dashboard', path: '/dashboard' },
    { label: 'File', path: '/file' },
    { label: 'Information', path: '/info' }
  ];

  const currentPath = location.pathname;

  const handleTabChange = (_event: React.SyntheticEvent, newValue: string) => {
    navigate(newValue);
  };

  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [hasNewNotifications, setHasNewNotifications] = useState<boolean>(false);

  useEffect(() => {
    setNotifications(notiList);
    if (notiList.length > 0) {
      setHasNewNotifications(true);
    }
  }, [notiList]);

  const handleNotificationClick = (event: React.MouseEvent<HTMLElement>) => {
    if (notiList.length > 0)
    setAnchorEl(event.currentTarget);
    setHasNewNotifications(false);
  };

  const handleNotificationClose = () => {
    setAnchorEl(null);
  };

  const openPopover = Boolean(anchorEl);
  const popoverId = openPopover ? 'notification-popover' : undefined;

  const getIcon = (type: string) => {
    switch (type) {
      case 'waiting':
        return <Pending />;
      case 'success':
        return <CheckCircle />;
      case 'error':
        return <Error />;
      default:
        return null;
    }
  };

  const getTextColor = (type: string) => {
    switch (type) {
      case 'waiting':
        return 'darkgoldenrod';
      case 'success':
        return 'darkgreen';
      case 'error':
        return 'darkred';
      default:
        return 'primary';
    }
  };

  const lastNotification = notifications.length > 0 ? notifications[0] : null;

  return (
    <ThemeProvider theme={theme}>
      <AppBar position="fixed" sx={{ boxShadow: 'true' }}>
        <Toolbar sx={{ minHeight: 48, padding: '0 !important', paddingRight: 1, height: "100%" }}>
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
                height: '100%',
                minWidth: 100,
                color: 'grey',
                textTransform: 'none',
                padding: 0,
                display: 'flex',
                alignItems: 'center',
                '&.Mui-selected': {
                  color: 'black',
                  backgroundColor: '#CEE5FD',
                },
                '&:hover': {
                  backgroundColor: 'lightgrey',
                },
                '&:not(:last-of-type)': {
                  borderRight: '1px solid grey',
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

          {lastNotification && (
            <TextField
              variant="outlined"
              size="small"
              value={lastNotification.message}
              InputProps={{
                startAdornment: getIcon(lastNotification.type),
                sx: { color: getTextColor(lastNotification.type) },
                readOnly: true,
              }}
              sx={{ marginRight: 2 }}
            />
          )}

          <IconButton onClick={handleNotificationClick} sx={{ marginRight: '10px' }}>
            <Badge color="error" variant="dot" invisible={!hasNewNotifications}>
              <NotificationsIcon />
            </Badge>
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
                  {getIcon(notification.type)}
                  <ListItemText sx={{ marginLeft: 1 }}
                    primary={notification.message}
                    primaryTypographyProps={{
                      sx: { color: getTextColor(notification.type) },
                    }}
                  />
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
