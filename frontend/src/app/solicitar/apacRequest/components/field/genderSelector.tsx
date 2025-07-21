import * as React from 'react';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import { useFormRequest } from "@/app/solicitar/apacRequest/contexts/FormApacRequest";
import { Controller } from 'react-hook-form';

export default function GenderSelector({disabled}: {disabled?: boolean}) {
    const { form } = useFormRequest();

    return (
        <Controller
            name="apacData.patientGender"
            control={form.control}
            render={({ field }) => (
            <FormControl fullWidth>
                <InputLabel id="gender-select-label">Sexo do paciente</InputLabel>
                <Select
                    id="gender-select"
                    label="Sexo do paciente"
                    disabled={disabled}
                    required
                    size="small" 
                    {...field}>
                    <MenuItem value="masculino">Masculino</MenuItem>
                    <MenuItem value="feminino">Feminino</MenuItem>
                </Select>
                </FormControl>
        )}/>
    );
}
