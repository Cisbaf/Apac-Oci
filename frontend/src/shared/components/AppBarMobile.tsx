import React, { useState } from 'react';
import {
  Box,
  Typography,
  Menu,
  MenuItem,
  IconButton,
  Divider,
  styled,
  ListItemIcon,
  ListItemText,
  Avatar,
} from "@mui/material";
import Image from "next/image";
import Link from "next/link";
import MenuIcon from '@mui/icons-material/Menu';
import logo from '../../../public/logo-cisbaf.png';
import { MenuItems } from './menu';
import { useRouter } from 'next/navigation';
import { useContextUser } from '../context/UserContext';

// Estilo do menu
const StyledMenu = styled(Menu)(({ theme }) => ({
  '& .MuiPaper-root': {
    backgroundColor: theme.palette.background.paper,
    minWidth: 240,
    boxShadow: '0px 4px 20px rgba(0, 0, 0, 0.15)',
    borderRadius: '10px',
    border: `1px solid ${theme.palette.divider}`,
  },
  '& .MuiMenuItem-root': {
    padding: '10px 18px',
    fontSize: '14px',
    borderRadius: 6,
    '&:hover': {
      backgroundColor: theme.palette.action.hover,
    },
  },
}));

export default function AppBarMobile() {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);
  const route = useRouter();
  const user = useContextUser();

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handlePage = (path: string) => {
    handleClose();
    route.push(path)
  }

  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        width: "100%",
        backgroundColor: "#343a40",
        paddingX: 2,
        paddingY: 1,
      }}
    >
      {/* Logo e título */}
      <Box>
        <Image src={logo.src} width={100} height={25} alt="Logo" />
        <Typography variant="body2" color="white">
          Sistema Apac OCI
        </Typography>
      </Box>

      {/* Botão de menu */}
      <Box sx={{ position: 'relative' }}>
        <IconButton
          size="large"
          sx={{
            paddingRight: 10,
            color: "white",
            '&:hover': { backgroundColor: 'rgba(255, 255, 255, 0.1)' },
          }}
          aria-label="menu"
          aria-controls={open ? 'mobile-menu' : undefined}
          aria-haspopup="true"
          aria-expanded={open ? 'true' : undefined}
          onClick={handleClick}
        >
          <MenuIcon />
        </IconButton>

        {/* Menu com seções */}
        <StyledMenu
          id="mobile-menu"
          anchorEl={anchorEl}
          open={open}
          onClose={handleClose}
          anchorOrigin={{
            vertical: 'bottom',
            horizontal: 'left',
          }}
          transformOrigin={{
            vertical: 'top',
            horizontal: 'left',
          }}
        >
         

          {/* Sessão futura (exemplo) */}
          <Box sx={{ px: 2, py: 1 }}>
            <Typography
              variant="subtitle2"
              sx={{
                fontWeight: 600,
                color: 'text.secondary',
                mb: 0.5,
                textTransform: 'uppercase',
              }}
            >
              Configurações
            </Typography>
            <Divider sx={{ mb: 1 }} />
      
            <MenuItem >
                <Box sx={{display: "flex", gap: 1}}>
                    <Avatar sx={{ width: 40, height: 40 }} />
                    <Typography mt={1} variant="body2">
                     { user.name }
                    </Typography>
                </Box>
            </MenuItem>
            <MenuItem onClick={()=>handlePage("admin")}>Painel de Administração</MenuItem>
            <MenuItem onClick={()=>handlePage("logout")}>Sair</MenuItem>
          </Box>
           {/* Sessão: Páginas */}
          <Box sx={{ px: 2, py: 1 }}>
            <Typography
              variant="subtitle2"
              sx={{
                fontWeight: 600,
                color: 'text.secondary',
                mb: 0.5,
                textTransform: 'uppercase',
              }}
            >
              Páginas
            </Typography>
            <Divider sx={{ mb: 1 }} />

            {MenuItems.map((menu, index) => (
              <MenuItem
                key={index}
                onClick={()=>handlePage(menu.route)}
                component={Link}
                href={menu.route}
              >
                <ListItemIcon sx={{ minWidth: 36 }}>
                  {menu.icon}
                </ListItemIcon>
                <ListItemText primary={menu.label} />
              </MenuItem>
            ))}
          </Box>
        </StyledMenu>
      </Box>
    </Box>
  );
}
