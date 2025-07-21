'use client';

import React, { useEffect } from 'react';
import {
  Box,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Collapse,
  Typography,
  Avatar,
  Divider,
  IconButton,
  Tooltip,
  Menu,
  MenuItem,
  useMediaQuery,
  useTheme,
  CircularProgress,
  Skeleton
} from '@mui/material';
import {
  Home,
  PlaylistAddCheck,
  FileDownload,
  Assignment,
  ExpandLess,
  ExpandMore,
  Menu as MenuIcon,
  ChevronLeft as ChevronLeftIcon,
  AppRegistration,
  FileOpen,
  HowToReg,
  AdminPanelSettings,
  Logout,
} from '@mui/icons-material';
import Image from 'next/image';
import logo from '../../../public/logo-cisbaf.png';
import { useRouter } from 'next/navigation';
import { UserRole } from '../schemas/user';
import { useContextUser } from '../context/UserContext';

interface MenuItemType {
  label: string;
  icon: React.ReactNode;
  route: string;
  viwer?: UserRole;
  subItems?: string[];
}

const drawerWidth = 300;
const collapsedWidth = 72;

const menuItems: MenuItemType[] = [
  { label: 'Home', icon: <Home />, route: '/' },
  { label: 'Solicitar Apac Oci', icon: <AppRegistration />, route: '/solicitar', viwer: UserRole.REQUESTER },
  { label: 'Autorizar APAC OCI', icon: <HowToReg />, route: '/responder', viwer: UserRole.AUTHORIZER},
  { label: 'Listagem de Solicitações', icon: <PlaylistAddCheck />, route: '/visualizar' },
  { label: 'Extração APAC-OCI de Solicitações', icon: <FileDownload />, route: '/', viwer: UserRole.REQUESTER },
  { label: 'Relatórios', icon: <Assignment />, route: '/', viwer: UserRole.ADMIN},
];

export default function Sidebar() {
  const [openItems, setOpenItems] = React.useState<{ [key: string]: boolean }>({});
  const [isOpen, setIsOpen] = React.useState(true);
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const theme = useTheme();
  const isTabletOrMobile = useMediaQuery(theme.breakpoints.down('md'));
  const route = useRouter();
  const user = useContextUser();

  // Fecha o menu em dispositivos pequenos ao montar
  useEffect(() => {
    if (isTabletOrMobile) setIsOpen(false);
  }, [isTabletOrMobile]);

  const toggleItem = (label: string) => {
    setOpenItems((prev) => ({ ...prev, [label]: !prev[label] }));
  };

  const handleAvatarClick = (event: any) => {
    setAnchorEl(event.currentTarget);
  };

  const handleCloseMenu = () => {
    setAnchorEl(null);
  };

  return (
    <Box
      sx={{
        width: isOpen ? drawerWidth : collapsedWidth,
        height: '100vh',
        backgroundColor: '#2f3b46',
        color: 'white',
        display: 'flex',
        flexDirection: 'column',
        transition: 'width 0.3s',
      }}
    >
      {/* Header */}
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: isOpen ? 'space-between' : 'center', p: 2 }}>
        {isOpen && (
          <Box>
            <Image src={logo.src} width={200} height={50} alt="Logo" />
            <Typography variant="h6" noWrap>
              Plataforma Cisbaf
            </Typography>
            <Typography variant="body2" noWrap>
              Sistema de APAC OCI
            </Typography>
          </Box>
        )}
        <IconButton onClick={() => setIsOpen(!isOpen)} sx={{ color: 'white' }}>
          {isOpen ? <ChevronLeftIcon /> : <MenuIcon />}
        </IconButton>
      </Box>

      {/* Avatar com Submenu */}

    
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', p: 1 }}>
        <Tooltip title="Opções do usuário">
          <IconButton onClick={handleAvatarClick}>
            <Avatar sx={{ width: 40, height: 40 }} />
          </IconButton>
        </Tooltip>
        {isOpen && (
          <Typography mt={1} variant="body2">
            { user.name }
          </Typography>
        )}
        <Menu
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={handleCloseMenu}
          anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
          transformOrigin={{ vertical: 'top', horizontal: 'center' }}
        >
          {user.role === UserRole.ADMIN &&
           <MenuItem onClick={handleCloseMenu}>
            <ListItemIcon>
              <AdminPanelSettings fontSize="small" />
            </ListItemIcon>
            <ListItemText>Painel de Administração</ListItemText>
          </MenuItem>
          }
          <MenuItem onClick={()=>route.push("/logout")}>
            <ListItemIcon>
              <Logout fontSize="small" />
            </ListItemIcon>
            <ListItemText>Sair</ListItemText>
          </MenuItem>
        </Menu>
      </Box>

      <Divider sx={{ bgcolor: 'rgba(255,255,255,0.2)', my: 1 }} />

      {isOpen && (
        <Typography sx={{ px: 2, py: 1, fontSize: 13, color: 'gray' }}>
          NAVEGAÇÃO PRINCIPAL
        </Typography>
      )}

      {/* Menu */}
      <List>
        {menuItems.map((item) => {
          const isExpanded = openItems[item.label];
          const hasSubItems = item.subItems && item.subItems.length > 0;
          if (item.viwer && item.viwer != user.role) return;
          return (
            <React.Fragment key={item.label}>
              <Tooltip
                title={!isOpen ? item.label : ''}
                placement="right">
                <ListItemButton
                  onClick={() => {
                    if ( hasSubItems) toggleItem(item.label);
                    else route.push(item.route);
                  }}
                  sx={{
                    justifyContent: isOpen ? 'flex-start' : 'center',
                    px: isOpen ? 2 : 1,
                    color: 'white',
                  }}
                >
                  <ListItemIcon sx={{ color: 'white', minWidth: 0, mr: isOpen ? 2 : 0, justifyContent: 'center' }}>
                    {item.icon}
                  </ListItemIcon>
                  {isOpen && <ListItemText primary={item.label} />}
                  {isOpen && hasSubItems && (isExpanded ? <ExpandLess /> : <ExpandMore />)}
                </ListItemButton>
              </Tooltip>

              {hasSubItems && (
                <Collapse in={isExpanded} timeout="auto" unmountOnExit>
                  <List component="div" disablePadding>
                    {item.subItems?.map((sub) => (
                      <ListItemButton key={sub} sx={{ pl: isOpen ? 4 : 2, color: 'white' }}>
                        <ListItemText primary={sub} />
                      </ListItemButton>
                    ))}
                  </List>
                </Collapse>
              )}
            </React.Fragment>
          );
        })}
      </List>
    </Box>
  );
}
