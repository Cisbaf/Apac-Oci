import React, { useEffect, useMemo, useRef, useState } from "react";
import { DataGrid, GridColDef } from "@mui/x-data-grid";
import VisibilityIcon from "@mui/icons-material/Visibility";
import { Box, IconButton, Button, ListItemIcon, ListItemText } from "@mui/material";
import { ApacRequest, ApacStatusTranslation } from "@/app/solicitar/apacRequest/schemas/apacRequest";
import { useContextUser } from "../context/UserContext";
import { useApacViewContext } from "../context/ApacViewContext";
import { useApacAuthorizationContext } from "@/app/responder/apacAuthorization/context/authorizationContext";
import { UserRole } from "../schemas/user";
import ApacModal from "./ApacModal";
import { ModalHandles } from "./Modal";
import { useAutorizeMultiplesApac } from "../context/AutorizeMultiplesApac";
import { ApacSelectCheckbox } from "./ApacSelectCheckbox";
import GradingIcon from '@mui/icons-material/Grading';
import ChecklistIcon from '@mui/icons-material/Checklist';
import PlaylistRemoveIcon from '@mui/icons-material/PlaylistRemove';
import { Menu, MenuItem } from "@mui/material";
import AppsIcon from '@mui/icons-material/Apps';


interface TableProps {
  onlyView?: boolean;
}

export default function ApacTable({ onlyView }: TableProps) {
  const user = useContextUser();
  const { listApac } = useApacViewContext();
  const { openModalAuthorization, toggleAll, clearSelection } = useAutorizeMultiplesApac();
  const { authorize } = useApacAuthorizationContext();
  const [selectedApac, setSelectedApac] = useState<ApacRequest | undefined>();
  const modalRef = useRef<ModalHandles>(null);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  const openMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const closeMenu = () => setAnchorEl(null);

  const handleView = (id: number) => {
    const found = listApac.find((apac) => apac.id === id);
    setSelectedApac(found);
  };
  
  const togleAllList = () => {
    const ids = listApac.map(apac => apac.id);
    toggleAll(ids);
  }

  const columns: GridColDef[] = useMemo(() => {
    const baseCols: GridColDef[] = [
      {
        field: "id",
        headerName: "",
        width: 40,
        sortable: false,
        filterable: false,
        renderCell: (params) => (
          <IconButton onClick={() => handleView(params.row.id)}>
            <VisibilityIcon />
          </IconButton>
        ),
      },
      { field: "name", headerName: "Nome Paciente", width: 150 },
      { field: "cns", headerName: "CNS Paciente", width: 150 },
      { field: "establishment", headerName: "Estabelecimento", width: 220},
      { field: "procedure", headerName: "Procedimento", width: 180 },
      { field: "status", headerName: "Status", width: 100 },
    ];

    if (user.role !== UserRole.GUEST && !onlyView) {
      baseCols.push({
        field: "action",
        headerName: "Ações",
        width: 250,
        sortable: false,
        filterable: false,
        
        renderHeader: () => (
        <>
          Ações
          <IconButton size="small" onClick={openMenu}>
            <AppsIcon fontSize="small" />
          </IconButton>
        </>
        ),
        renderCell: (params) => {
          const rowData = params.row;
          if (rowData.status !== "Pendente") return null;

          return (
            <Box display="flex" gap={1}>
              <Button
                color="error"
                variant="contained"
                size="small"
                onClick={()=>authorize(rowData.id, "reject")}>Rejeitar</Button>
              <Button
                color="success"
                variant="contained"
                size="small"
                onClick={()=>authorize(rowData.id, "approved")}>Aprovar</Button>

              <ApacSelectCheckbox id={rowData.id}/>
            </Box>
          );
        },
      });
    }

    return baseCols;
  }, [onlyView, listApac]);

  const rows = useMemo(() => {
    return listApac.map((apac) => ({
      id: apac.id,
      name: apac.apac_data.patient_data.name,
      cns: apac.apac_data.patient_data.cns,
      establishment: apac.establishment.name,
      procedure: apac.apac_data.main_procedure.name,
      status: ApacStatusTranslation[apac.status],
    }));
  }, [listApac]);

  useEffect(() => {
    if (selectedApac) {
      modalRef.current?.openModal();
    }
  }, [selectedApac]);

  if (!(rows.length > 0)) return <></>;

  return (
    <Box>
      <Box sx={{  width: "100%" }}>
        <DataGrid
          rows={rows}
          columns={columns}
          initialState={{
            pagination: {
              paginationModel: { pageSize: 5 },
            },
          }}
          pageSizeOptions={[5, 10, 20, 50]}
        />
      </Box>

    <Menu
      anchorEl={anchorEl}
      open={Boolean(anchorEl)}
      onClose={closeMenu}
      anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
      transformOrigin={{ vertical: "top", horizontal: "right" }}
    >
      <MenuItem
        onClick={() => {
          openModalAuthorization();
          closeMenu();
        }}
      >
        <ListItemIcon>
          <GradingIcon fontSize="small" />
        </ListItemIcon>

        <ListItemText
          primary="Autorizar OCIs marcadas"
          primaryTypographyProps={{ fontSize: 14 }}
        />
      </MenuItem>

       <MenuItem
        onClick={() => {
          togleAllList();
          closeMenu();
        }}
      >
        <ListItemIcon>
          <ChecklistIcon fontSize="small" />
        </ListItemIcon>

        <ListItemText
          primary="Selecionar toda lista"
          primaryTypographyProps={{ fontSize: 14 }}
        />
      </MenuItem>

       <MenuItem
        onClick={() => {
          clearSelection();
          closeMenu();
        }}
      >
        <ListItemIcon>
          <PlaylistRemoveIcon fontSize="small" />
        </ListItemIcon>

        <ListItemText
          primary="Desmarcar toda lista"
          primaryTypographyProps={{ fontSize: 14 }}
        />
      </MenuItem>
    </Menu>


      {selectedApac && (
        <ApacModal
          ref={modalRef}
          apacRequest={selectedApac}
          onClose={() => setSelectedApac(undefined)}
        />
      )}
    </Box>
  );
}
