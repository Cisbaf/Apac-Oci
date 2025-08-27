import * as React from 'react';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import { useFormRequest } from "@/app/solicitar/apacRequest/contexts/FormApacRequest";
import { Controller } from 'react-hook-form';

export default function RaceColorSelector({disabled}: {disabled?: boolean}) {
const { form } = useFormRequest();

  return (
    <Controller
        name="apacData.patientRaceColor"
        control={form.control}
        render={({ field }) => (
        <FormControl fullWidth>
            <InputLabel id="race-color-select-label">Raça/Cor</InputLabel>
            <Select
              id="race-color-select"
              label="Raça/Cor"
              required
              size="small"
              disabled={disabled}
              {...field}>
              <MenuItem value="01">Branca</MenuItem>
              <MenuItem value="02">Preta</MenuItem>
              <MenuItem value="03">Parda</MenuItem>
              <MenuItem value="04">Amarela</MenuItem>
              <MenuItem value="05">Indígena</MenuItem>
            </Select>
          </FormControl>
    )}/>

  );
}
