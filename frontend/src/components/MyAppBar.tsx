import React from 'react';
import {
  AppBar as MuiAppBar,
  Toolbar,
  IconButton,
} from '@mui/material';
import { styled } from '@mui/material/styles';
import MenuIcon from '@mui/icons-material/Menu';

const drawerWidth = 240;

const AppBarWrapper = styled(MuiAppBar, { shouldForwardProp: (prop) => prop !== 'open', })<{
  open?: boolean;
}>(({ theme, open }) => ({
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

const MyAppBar: React.FC<AppBarProps> = ({ open, toggleDrawer }) => (
  <AppBarWrapper position="absolute" open={open} sx={{background: 'none', boxShadow: 'none'}}>
    <Toolbar>
      <IconButton
        edge="start"
        aria-label="open drawer"
        onClick={toggleDrawer}
        sx={{
          marginRight: '36px',
          color: "grey",
          ...(open && { display: 'none' }),
        }}
      >
        <MenuIcon />
      </IconButton>
      {/* <IconButton color="inherit">
        <Badge badgeContent={4} color="secondary">
          <NotificationsIcon />
        </Badge>
      </IconButton> */}
    </Toolbar>
  </AppBarWrapper>
);

export default MyAppBar;