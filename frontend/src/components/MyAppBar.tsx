import React from 'react';
import { AppBar as MuiAppBar, Toolbar, IconButton, Tabs, Tab } from '@mui/material';
import { styled } from '@mui/material/styles';
import MenuIcon from '@mui/icons-material/Menu';
import { useLocation, useNavigate } from 'react-router-dom';

const drawerWidth: number = 300; // Width of the drawer

// Styled component for the AppBar with conditional styling based on the 'open' prop
const AppBarWrapper = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== 'open',
})<{ open?: boolean }>(({ theme, open }) => ({
  zIndex: theme.zIndex.drawer + 1,
  transition: theme.transitions.create(['width', 'margin'], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  ...(open && {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  }),
}));

interface AppBarProps {
  open: boolean;
  toggleDrawer: () => void;
  openable: boolean;
}

// Functional component for the AppBar
const MyAppBar: React.FC<AppBarProps> = ({ open, toggleDrawer, openable }) => {
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

  return (
    <AppBarWrapper position="absolute" open={open} sx={{ background: '#F3F3F3', boxShadow: 'none'}}>
      <Toolbar sx={{ minHeight: 48, padding: '0 !important', height: "100%"}}>
        {/* Menu button to toggle the drawer */}
        <IconButton
          edge="start"
          aria-label="open drawer"
          onClick={toggleDrawer}
          sx={{
            marginRight: '36px',
            marginLeft: '36px',
            color: 'grey',
            ...((open || !openable) && { display: 'none' }), // Hide button when drawer is open
          }}
        >
          <MenuIcon />
        </IconButton>

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
      </Toolbar>
    </AppBarWrapper>
  );
};

export default MyAppBar;
