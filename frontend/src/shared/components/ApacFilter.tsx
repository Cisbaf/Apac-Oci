import React from "react";
import {
  Box,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Button,
} from "@mui/material";
import { useApacViewContext } from "../context/ApacViewContext";
import { useAutorizeMultiplesApac } from "../context/AutorizeMultiplesApac";

const statusOptions = [
  { label: "Solicitadas", value: "pending" },
  { label: "Aprovadas", value: "approved" },
  { label: "Negadas", value: "rejected" },
];

export default function ApacFilter() {

  const {clearSelection} = useAutorizeMultiplesApac();
  // Obtem a data atual
  const today = new Date();
  const todayStr = today.toISOString().split("T")[0];

  // Define o primeiro dia do mês atual
  const firstDayOfMonth = new Date(today.getFullYear(), today.getMonth(), 1)
    .toISOString()
    .split("T")[0];

  const [dataInicio, setDataInicio] = React.useState<string>(firstDayOfMonth);
  const [dataFim, setDataFim] = React.useState<string>(todayStr);
  const [status, setStatus] = React.useState<string>("pending");
  const { searchApacs } = useApacViewContext();

  const makeParams = () => {
    clearSelection();
    const params = `start_date=${dataInicio}&end_date=${dataFim}&status=${status}`;
    searchApacs(params);
  };

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "row",
        flexWrap: "wrap",
        gap: 2,
        alignItems: "center",
        padding: 2,
        border: "1px solid #ccc",
        borderRadius: 1,
      }}
    >
      <TextField
        size="small"
        label="Data Início"
        type="date"
        value={dataInicio}
        onChange={(e) => setDataInicio(e.target.value)}
        InputLabelProps={{ shrink: true }}
      />
      <TextField
        size="small"
        label="Data Fim"
        type="date"
        value={dataFim}
        onChange={(e) => setDataFim(e.target.value)}
        InputLabelProps={{ shrink: true }}
      />
      <FormControl sx={{ minWidth: 150 }}>
        <InputLabel id="select-status-label">Status</InputLabel>
        <Select
          labelId="select-status-label"
          value={status}
          label="Status"
          onChange={(e) => setStatus(e.target.value)}
        >
          {statusOptions.map((option) => (
            <MenuItem key={option.value} value={option.value}>
              {option.label}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <Button variant="contained" onClick={makeParams} sx={{ height: 40 }}>
        Pesquisar
      </Button>
    </Box>
  );
}
