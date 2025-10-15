import React from "react";
import CardForm from "@/shared/components/CardForm";
import { TextField, Grid, Box, FormControl, InputLabel, Select, MenuItem } from "@mui/material";
import { Controller, useWatch } from 'react-hook-form';
import { useFormRequest } from "@/app/solicitar/apacRequest/contexts/FormApacRequest";
import { FormRepository, FormProps } from "@/shared/repositories/formRepository";
import { MESSAGENOTCHECKVALIDITY } from "@/app/solicitar/apacRequest/utils/messages";
import { useRequestData } from "@/app/solicitar/apacRequest/contexts/ApacRequestContext";


const IdentifyEstablishmentForm = React.forwardRef<FormRepository, FormProps>((props, ref)=>{
    const formRef = React.useRef<HTMLFormElement>(null);
    const { form, disabled: disabledForm } = useFormRequest();
    const disabled = props.disabled? props.disabled : disabledForm;
    const { control, getValues } = form;
    const { establishments } = useRequestData();
    const establishmentId = useWatch({
        control,
        name: "establishmentId"
    });
    const [textCnes, setTextCnes] = React.useState("");

    React.useImperativeHandle(ref, ()=>({
        validate() {
            if(formRef.current && !formRef.current.checkValidity()){
                formRef.current.reportValidity();
                return { success: false, message: MESSAGENOTCHECKVALIDITY };
            }
            if (getValues("establishmentId") <= 0) return {success: false, message: "Selecione um estabelecimento valído!"};
            return { 
                success: true,
                message: "Formulário correto!"
            };
        },
    }));

    React.useEffect(()=>{
        const establishment = establishments.find(e=>e.id === establishmentId);
        if (establishment) setTextCnes(establishment.cnes);
    }, [establishmentId]);

    return(
        <CardForm
            title="Identificação do estabelecimento de Saúde"
            contentBoxStyle={{
                padding: 4
            }}>
            <Box 
                ref={formRef} 
                component="form"
                onSubmit={(e)=>e.preventDefault()}>
                <Grid container spacing={3}>
                    <Grid size={{xs:12, sm:6}}>
                        <Controller
                            name="establishmentId"
                            control={ control }
                            render={({ field }) => (
                            <FormControl fullWidth>
                                <InputLabel id="establishment-select-label">
                                    Nome do estabelecimento de Saúde
                                </InputLabel>
                                <Select
                                data-testid="select-establishment"
                                id="establishment-select"
                                label="Nome do estabelecimento de Saúde"
                                disabled={disabled}
                                required
                                {...field}>
                                <MenuItem value={0} disabled>
                                    <em>Selecione um Estabelecimento</em>
                                </MenuItem>
                                {establishments.map(establishment=>(
                                <MenuItem
                                    key={establishment.cnes}
                                    value={establishment.id}
                                    sx={{
                                    whiteSpace: 'normal',     // 🔹 Permite quebra de linha
                                    wordBreak: 'break-word',  // 🔹 Quebra palavras longas
                                    lineHeight: 1.3,          // 🔹 Opcional: melhora espaçamento entre linhas
                                    }}
                                    >
                                    {establishment.name}
                                </MenuItem>
                                ))}
                                </Select>
                            </FormControl>
                    )}/>
                    </Grid>
                    <Grid size={{xs:12, sm:6}}>
                        <TextField   size="small" 
                            label="CNES"
                            type="number"
                            value={textCnes}
                            disabled
                            fullWidth
                            required/>
                    </Grid>
                </Grid>
            </Box>
        </CardForm>
        
    )
});

export default IdentifyEstablishmentForm;