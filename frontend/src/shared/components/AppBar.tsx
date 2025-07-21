import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import NotificationsIcon from '@mui/icons-material/Notifications';
import { Badge } from '@mui/material';

export default function ButtonAppBar() {
  return (
   <AppBar position="static" color='default' sx={{backgroundColor: "white"}}>
        <Toolbar sx={{display: "flex", justifyContent: "flex-end"}}>
            {/* <IconButton size="large" aria-label="show 4 new mails" color="inherit" sx={{}}>
              <Badge badgeContent={4} color="error">
                <NotificationsIcon />
              </Badge>
            </IconButton> */}
        </Toolbar>
      </AppBar>
  );
}