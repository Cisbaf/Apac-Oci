import React from 'react';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import dayjs from 'dayjs';
import 'dayjs/locale/pt-br';
import { Controller } from 'react-hook-form';
import { useFormRequest } from "@/app/solicitar/apacRequest/contexts/FormApacRequest";

dayjs.locale('pt-br');

interface DateSelector {
  formKey: "procedure"|"discharge";
  disabled?: boolean;
}

function DateSelector(props: DateSelector) {
  const { form } = useFormRequest();
  const { control } = form;
  const chv = {
    procedure: {form: "apacData.procedureDate", label: "Data do Procedimento"},
    discharge: {form: "apacData.dischargeDate", label: "Data da Alta"},
} as const;

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale="pt-br">
      <Controller
        name={chv[props.formKey].form}
        control={control}
        defaultValue=""
        rules={{
          required: `${chv[props.formKey].label} é obrigatoria`,
          validate: (value) => {
            if (!value) return true; // Se vazio, o required já trata
            return dayjs(value, 'DD/MM/YYYY', true).isValid() || 'Data inválida';
          }
        }}
        render={({ field, fieldState: { error } }) => (
          <DatePicker
            sx={{}}
            label={chv[props.formKey].label}
            value={field.value ? dayjs(field.value, 'DD/MM/YYYY') : null}
            onChange={(date) => {
              const formatted = date ? date.format('DD/MM/YYYY') : '';
              field.onChange(formatted);
            }}
            format="DD/MM/YYYY"
            slotProps={{
              textField: {
                helperText: error?.message || props.disabled? "" : 'Formato: dd/mm/aaaa',
                error: !!error, // Isso ativa o estado de erro visual
                fullWidth: true,
                required: true, // Adiciona o asterisco vermelho
              },
            }}
            disabled={props.disabled}
          />
        )}
      />
    </LocalizationProvider>
  );
}

export default DateSelector;