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
import MonthYearInputGeneric from "./MontYearInputGeneric";

const statusOptions = [
  { label: "Solicitadas", value: "pending" },
  { label: "Aprovadas", value: "approved" },
  { label: "Negadas", value: "rejected" },
];

export default function ApacFilter() {
  const {clearSelection} = useAutorizeMultiplesApac();
  const [status, setStatus] = React.useState<string>("pending");
  const { searchApacs } = useApacViewContext();
  const [productionValue, setProductionValue] = React.useState<Date | null>(null);

  const makeParams = () => {
    clearSelection();
    console.log(productionValue)
    const params = new URLSearchParams({
      competencia_month: productionValue
        ? String(productionValue.getMonth() + 1).padStart(2, "0")
        : "",
        
      competencia_year: productionValue
        ? String(productionValue.getFullYear())
        : "",

      status,
    }).toString();
    searchApacs(params);
  };

    const now = new Date();
    const currentMonth = String(now.getMonth() + 1).padStart(2, "0");
    const currentYear = now.getFullYear();
    const maxDate = `${currentYear}-${currentMonth}`;

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
    <Box flex={0.5}>
    <MonthYearInputGeneric
      minDate="2024-01"
      maxDate={maxDate}
      value={productionValue}
      setValue={setProductionValue}
      label="Período de Produção"/>
      </Box>
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
