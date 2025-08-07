import React, { useEffect, useMemo, useRef, useState } from "react";
import { DataGrid, GridColDef } from "@mui/x-data-grid";
import VisibilityIcon from "@mui/icons-material/Visibility";
import { Box, IconButton, Button } from "@mui/material";
import { ApacRequest, ApacStatusTranslation } from "@/app/solicitar/apacRequest/schemas/apacRequest";
import { useContextUser } from "../context/UserContext";
import { useApacViewContext } from "../context/ApacViewContext";
import { useApacAuthorizationContext } from "@/app/responder/apacAuthorization/context/authorizationContext";
import { UserRole } from "../schemas/user";
import ApacModal from "./ApacModal";
import { ModalHandles } from "./Modal";

interface TableProps {
  onlyView?: boolean;
}

export default function ApacTable({ onlyView }: TableProps) {
  const user = useContextUser();
  const { listApac } = useApacViewContext();
  const { authorize } = useApacAuthorizationContext();
  const [selectedApac, setSelectedApac] = useState<ApacRequest | undefined>();
  const modalRef = useRef<ModalHandles>(null);

  const handleView = (id: number) => {
    const found = listApac.find((apac) => apac.id === id);
    setSelectedApac(found);
  };

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
      { field: "request_date", headerName: "Data da Solicitação", width: 180 },
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
      request_date: apac.request_date,
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
      <Box sx={{ height: 400, width: "100%" }}>
        <DataGrid
          rows={rows}
          columns={columns}
          initialState={{
            pagination: {
              paginationModel: { pageSize: 5 },
            },
          }}
          pageSizeOptions={[5]}
        />
      </Box>

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
