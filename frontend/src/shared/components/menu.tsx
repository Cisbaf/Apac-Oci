import { UserRole } from "../schemas/user";
import {
  Home,
  PlaylistAddCheck,
  FileDownload,
  Menu as MenuIcon,
  ChevronLeft as ChevronLeftIcon,
  AppRegistration,
  HowToReg,
} from '@mui/icons-material';


interface MenuItemType {
  label: string;
  icon: React.ReactNode;
  route: string;
  viwer?: UserRole | UserRole[]; // <-- pode ser um ou vários
  subItems?: string[];
}

export const MenuItems: MenuItemType[] = [
  { label: 'Home', icon: <Home />, route: '/' },
  { label: 'Solicitar Apac Oci', icon: <AppRegistration />, route: '/solicitar', viwer: [UserRole.REQUESTER, UserRole.ADMIN] },
  { label: 'Autorizar APAC OCI', icon: <HowToReg />, route: '/responder', viwer: [UserRole.AUTHORIZER, UserRole.ADMIN] },
  { label: 'Listagem de Solicitações', icon: <PlaylistAddCheck />, route: '/visualizar' },
  { label: 'Extração APAC-OCI de Solicitações', icon: <FileDownload />, route: '/extracao', viwer: [UserRole.REQUESTER, UserRole.ADMIN] },
  // { label: 'Relatórios', icon: <Assignment />, route: '/', viwer: UserRole.ADMIN},
];