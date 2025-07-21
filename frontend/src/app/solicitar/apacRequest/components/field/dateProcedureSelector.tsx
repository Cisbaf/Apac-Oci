import React from 'react';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import dayjs from 'dayjs';
import 'dayjs/locale/pt-br';
import { Controller } from 'react-hook-form';
import { useFormRequest } from "@/app/solicitar/apacRequest/contexts/FormApacRequest";

dayjs.locale('pt-br');

function DateProcedureSelector({ disabled }: { disabled?: boolean }) {
  const { form } = useFormRequest();
  const { control } = form;

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale="pt-br">
      <Controller
        name="apacData.procedureDate"
        control={control}
        defaultValue=""
        rules={{
          required: 'Data do procedimento é obrigatória',
          validate: (value) => {
            if (!value) return true; // Se vazio, o required já trata
            return dayjs(value, 'DD/MM/YYYY', true).isValid() || 'Data inválida';
          }
        }}
        render={({ field, fieldState: { error } }) => (
          <DatePicker
            sx={{}}
            label="Data do Procedimento"
            value={field.value ? dayjs(field.value, 'DD/MM/YYYY') : null}
            onChange={(date) => {
              const formatted = date ? date.format('DD/MM/YYYY') : '';
              field.onChange(formatted);
            }}
            format="DD/MM/YYYY"
            slotProps={{
              textField: {
                helperText: error?.message || disabled? "" : 'Formato: dd/mm/aaaa',
                error: !!error, // Isso ativa o estado de erro visual
                fullWidth: true,
                required: true, // Adiciona o asterisco vermelho
              },
            }}
            disabled={disabled}
          />
        )}
      />
    </LocalizationProvider>
  );
}

export default DateProcedureSelector;