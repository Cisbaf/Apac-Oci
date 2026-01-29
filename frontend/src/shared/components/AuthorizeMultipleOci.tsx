import React from "react";
import {
  Button,
  Box,
  List,
  ListItem,
  ListItemAvatar,
  Avatar,
  ListItemText,
  IconButton,
  Typography
} from "@mui/material";
import { useApacViewContext } from "../context/ApacViewContext";
import { useAutorizeMultiplesApac } from "../context/AutorizeMultiplesApac";
import DeleteIcon from "@mui/icons-material/Delete";
import { useContextUser } from "../context/UserContext";
import { useGlobalComponents } from "../context/GlobalUIContext";
import MedicalInformationIcon from '@mui/icons-material/MedicalInformation';
import LocalHospitalIcon from "@mui/icons-material/LocalHospital";
import CalendarMonthIcon from "@mui/icons-material/CalendarMonth";
import HealingIcon from "@mui/icons-material/Healing";

export default function AuthorizeMultipleOci() {
  const { selected, removeOne } = useAutorizeMultiplesApac();
  const { listApac, getApacById, removeApac } = useApacViewContext();
  const { showBackdrop, showAlert } = useGlobalComponents();
  const { id: userID } = useContextUser();

  const [isAuthorizing, setIsAuthorizing] = React.useState(false);
  const [progress, setProgress] = React.useState({ current: 0, total: 0 });

  const cancelRef = React.useRef(false);

  const wait = (ms: number) =>
    new Promise<void>((resolve) => setTimeout(resolve, ms));

  // 🔐 Autoriza UM item e retorna sucesso ou falha
  const authorizeByID = async (id: number) => {
    try {
      const apacRequest = getApacById(id);

      showBackdrop(true, `Aprovando ...`);

      const response = await fetch("/api/proxy/apac_request/approved", {
        method: "POST",
        body: JSON.stringify({
          apac_request_id: id,
          authorizer_id: userID,
        }),
      });

      const response_json = await response.json();

      showBackdrop(false);

      if (!response.ok) throw new Error(response_json.message);

      removeOne(id);
      removeApac(apacRequest!);

      return true;
    } catch (error) {
      
      showBackdrop(false);
      
      showAlert({color: "error", message: `Erro ao autorizar. Processo interrompido.\n Detalhes: ${error}`});
      return false;
    }
  };

  // 🚦 Processo em fila
  const startAuthorization = async () => {
    if (selected.length === 0) return;

    setIsAuthorizing(true);
    cancelRef.current = false;
    setProgress({ current: 0, total: selected.length });

    for (let i = 0; i < selected.length; i++) {
      const id = selected[i];

      if (cancelRef.current) {
        showAlert({color: "info", message: "Autorizações canceladas pelo usuário."});
        break;
      }

      setProgress((p) => ({ ...p, current: i + 1 }));

      const success = await authorizeByID(id);

      if (!success) break;

      // Espera 2 segundos entre cada (checando cancelamento a cada 1s)
      if (i < selected.length - 1) {
        for (let s = 0; s < 2; s++) {
          if (cancelRef.current) break;
          await wait(1000);
        }
      }
    }

    setIsAuthorizing(false);
    setProgress({ current: 0, total: 0 });
  };

  // 🛑 Cancelamento manual
  const stopAuthorization = () => {
    cancelRef.current = true;
  };

  // 🧼 Cancela se o componente desmontar
  React.useEffect(() => {
    return () => {
      cancelRef.current = true;
    };
  }, []);

  return (
    <Box>
      <List sx={{ width: "100%", maxHeight: "400px", bgcolor: "background.paper", overflow: "auto" }}>
        {selected.map((id) => {
          const apacRequest = getApacById(id);
          return (
            <ListItem
              key={id}
              secondaryAction={
                !isAuthorizing && (
                  <IconButton edge="end" onClick={() => removeOne(id)}>
                    <DeleteIcon />
                  </IconButton>
                )
              }
            >
              <ListItemAvatar>
                <Avatar>
                  <MedicalInformationIcon />
                </Avatar>
              </ListItemAvatar>
              <ListItemText
                primary={
                  <Typography fontWeight={600}>
                    {apacRequest?.apac_data.patient_data.name}
                  </Typography>
                }
                secondary={
                  <Box display="flex" flexDirection="column" gap={0.5} mt={0.5}>
                    
                    <Box display="flex" alignItems="center" gap={1}>
                      <HealingIcon sx={{ fontSize: 16, opacity: 0.7 }} />
                      <Typography variant="body2">
                        {apacRequest?.apac_data.main_procedure.name}
                      </Typography>
                    </Box>

                    <Box display="flex" alignItems="center" gap={1}>
                      <LocalHospitalIcon sx={{ fontSize: 16, opacity: 0.7 }} />
                      <Typography variant="body2" color="text.secondary">
                        {apacRequest?.establishment.name}
                      </Typography>
                    </Box>

                    <Box display="flex" alignItems="center" gap={1}>
                      <CalendarMonthIcon sx={{ fontSize: 16, opacity: 0.7 }} />
                      <Typography variant="body2" color="text.secondary">
                        {apacRequest?.apac_data.procedure_date}
                      </Typography>
                    </Box>

                  </Box>
                }
              />

            </ListItem>
          );
        })}
      </List>

      {isAuthorizing && (
        <Typography sx={{ mt: 2 }}>
          Autorizando {progress.current} de {progress.total}
        </Typography>
      )}

      <Box mt={2}>
        {!isAuthorizing ? (
          <Button
            variant="contained"
            color="success"
            onClick={startAuthorization}
            disabled={selected.length === 0}
            fullWidth
          >
            Autorizar Todos
          </Button>
        ) : (
          <Button
            variant="contained"
            color="error"
            onClick={stopAuthorization}
            fullWidth
          >
            Parar autorizações
          </Button>
        )}
      </Box>
    </Box>
  );
}
