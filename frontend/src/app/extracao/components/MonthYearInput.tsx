import React, { useMemo } from "react";
import { TextField } from "@mui/material";
import { useExportContext } from "@/app/extracao/contexts/ExportContext";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import dayjs from "dayjs";
import "dayjs/locale/pt-br";

dayjs.locale("pt-br");

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

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale="pt-br">
      <DatePicker
        views={["month", "year"]}
        label={label}
        value={
          hookExtractForm.productionValue
            ? dayjs(hookExtractForm.productionValue)
            : null
        }
        onChange={(newValue) => {
          if (newValue) hookExtractForm.setProduction(newValue.toDate());
        }}
        minDate={minDate ? dayjs(minDate) : undefined}
        maxDate={maxDate ? dayjs(maxDate) : undefined}
        slotProps={{
          textField: {
            fullWidth: true,
            InputLabelProps: { shrink: true },
          },
        }}
      />
    </LocalizationProvider>
  );
};

export default MonthYearInput;