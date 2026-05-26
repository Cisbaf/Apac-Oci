import React from "react";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import dayjs, { Dayjs } from "dayjs";
import "dayjs/locale/pt-br";

dayjs.locale("pt-br");

interface MonthYearInputGenericProps {
  /** Valor atual */
  value: Date | null;

  /** Atualiza o valor */
  setValue: (date: Date | null) => void;

  /** Limite mínimo do campo (formato YYYY-MM) */
  minDate?: string;

  /** Limite máximo do campo (formato YYYY-MM) */
  maxDate?: string;

  /** Label customizado */
  label?: string;
}

const MonthYearInputGeneric: React.FC<MonthYearInputGenericProps> = ({
  value,
  setValue,
  minDate,
  maxDate,
  label = "Competência",
}) => {
  return (
    <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale="pt-br">
      <DatePicker
        views={["month", "year"]}
        label={label}
        value={value ? dayjs(value) : null}
        onChange={(newValue: Dayjs | null) => {
          setValue(newValue ? newValue.toDate() : null);
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

export default MonthYearInputGeneric;