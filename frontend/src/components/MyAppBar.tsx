import React from 'react';
import { AppBar as MuiAppBar, Toolbar, IconButton } from '@mui/material';
import { styled } from '@mui/material/styles';
import MenuIcon from '@mui/icons-material/Menu';

const drawerWidth = 240; // Width of the drawer

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
}

// Functional component for the AppBar
const MyAppBar: React.FC<AppBarProps> = ({ open, toggleDrawer }) => (
  <AppBarWrapper position="absolute" open={open} sx={{ background: 'none', boxShadow: 'none' }}>
    <Toolbar>
      {/* Menu button to toggle the drawer */}
      <IconButton
        edge="start"
        aria-label="open drawer"
        onClick={toggleDrawer}
        sx={{
          marginRight: '36px',
          color: "grey",
          ...(open && { display: 'none' }), // Hide button when drawer is open
        }}
      >
        <MenuIcon />
      </IconButton>
      {/* Placeholder for additional icons or content */}
      {/* <IconButton color="inherit">
        <Badge badgeContent={4} color="secondary">
          <NotificationsIcon />
        </Badge>
      </IconButton> */}
    </Toolbar>
  </AppBarWrapper>
);

export default MyAppBar;
