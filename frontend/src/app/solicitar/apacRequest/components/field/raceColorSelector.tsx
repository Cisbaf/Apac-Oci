import * as React from 'react';
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';
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
              <MenuItem value="branca">Branca</MenuItem>
              <MenuItem value="preta">Preta</MenuItem>
              <MenuItem value="parda">Parda</MenuItem>
              <MenuItem value="amarela">Amarela</MenuItem>
              <MenuItem value="indigena">Indígena</MenuItem>
            </Select>
          </FormControl>
    )}/>

  );
}
