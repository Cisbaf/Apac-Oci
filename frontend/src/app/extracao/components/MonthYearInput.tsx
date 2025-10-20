import React, { useMemo } from "react";
import { TextField } from "@mui/material";
import { useExportContext } from "@/app/extracao/contexts/ExportContext";

interface MonthYearInputProps {
  /** Limite mínimo do campo (formato YYYY-MM) */
  minDate?: string;
  /** Limite máximo do campo (formato YYYY-MM) */
  maxDate?: string;
  /** Label customizado */
  label?: string;
}

const MonthYearInput: React.FC<MonthYearInputProps> = ({
  minDate,
  maxDate,
  label = "Competência",
}) => {
  const { hookExtractForm } = useExportContext();

  // Função auxiliar: converte Date -> "YYYY-MM"
  const formatMonthInput = (date?: Date | null): string => {
    if (!date) return "";
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0"); // garante zero à esquerda
    return `${year}-${month}`;
  };

  // Função auxiliar: converte "YYYY-MM" -> Date
  const parseMonthInput = (value: string): Date | null => {
    const [year, month] = value.split("-");
    if (!year || !month) return null;
    return new Date(Number(year), Number(month) - 1, 1);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const date = parseMonthInput(e.target.value);
    if (date) {
      hookExtractForm.setProduction(date);
    }
  };

  // Define limites padrão se não forem passados por props
  const now = useMemo(() => new Date(), []);
  const defaultMin = `${now.getFullYear()}-01`;
  const defaultMax = formatMonthInput(now);

  const value = formatMonthInput(hookExtractForm.productionValue);

  return (
    <TextField
      label={label}
      type="month"
      value={value}
      onChange={handleChange}
      sx={{ display: "flex" }}
      InputLabelProps={{ shrink: true }}
      inputProps={{
        min: minDate || defaultMin,
        max: maxDate || defaultMax,
      }}
    />
  );
};

export default MonthYearInput;
