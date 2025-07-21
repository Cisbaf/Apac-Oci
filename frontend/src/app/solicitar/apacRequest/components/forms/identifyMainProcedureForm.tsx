import React from "react";
import CardForm from "@/shared/components/CardForm";
import { Grid, FormControl, InputLabel, Select, MenuItem, Typography, Box } from "@mui/material";
import { useFormRequest } from "@/app/solicitar/apacRequest/contexts/FormApacRequest";
import { FormRepository, FormProps } from "@/shared/repositories/formRepository";
import { MESSAGENOTCHECKVALIDITY } from "@/app/solicitar/apacRequest/utils/messages";
import { Controller, useWatch } from 'react-hook-form';
import DateProcedureSelector from "../field/dateProcedureSelector";
import { useRequestData } from "@/app/solicitar/apacRequest/contexts/ApacRequestContext";

const IdentifyMainProcedure = React.forwardRef<FormRepository, FormProps>((props, ref)=>{
    const formRef = React.useRef<HTMLFormElement>(null);
    const { form, disabled:disabledForm } = useFormRequest();
    const { control, getValues } = form;
    const { procedures } = useRequestData();
    const disabled = props.disabled? props.disabled : disabledForm;
    const procedureId = useWatch({
        control,
        name: "apacData.mainProcedureId"
    });
      
    React.useImperativeHandle(ref, ()=>({
        validate() {
            if(formRef.current && !formRef.current.checkValidity()){
                formRef.current.reportValidity();
                return { success: false, message: MESSAGENOTCHECKVALIDITY };
            }
            if (getValues("apacData.mainProcedureId") <= 0) return {success: false, message: "Selecione um procedimento valído!"};
            return { 
                success: true,
                message: "Formulário correto!"
            };
        },
    }));

    const getProcedure = () => {
        const procedure = procedures.find(p=>p.id === procedureId);
        if (procedure) return `${procedure.code} - ${procedure.name}`;
        return ""
    }

    return(
        <CardForm
            title="Procedimento Solicitado"
            contentBoxStyle={{
                padding: 4,

            }}>
            <Box 
                ref={formRef} 
                component="form"
                onSubmit={(e)=>e.preventDefault()}>
                <Grid container spacing={3}>
                    <Grid size={{xs:12, sm:6}}>
                        {disabled? (
                        <Box sx={{
                            height: "100%",
                            display: "flex",
                            flexDirection: "column",
                            gap: 1,
                        }}>
                            <Typography
                                color="textDisabled"
                                variant="h6">
                                Procedimento
                            </Typography>
                            <Typography
                                color="textDisabled"
                                variant="body1">
                                {getProcedure()}
                            </Typography>
                        </Box>
                        ):(
                        <Controller
                            name="apacData.mainProcedureId"
                            control={control}
                            render={({ field }) => (
                            <FormControl fullWidth>
                                <InputLabel id="procedure-select-label">
                                    Procedimento
                                </InputLabel>
                                <Select
                                    data-testid="select-procedure"
                                    id="procedure-select"
                                    label="Procedimento"
                                    disabled={disabled}
                                    required
                                    {...field}>
                                    <MenuItem value={0} disabled>
                                        <em>Selecione um Procedimento</em>
                                    </MenuItem>
                                    {procedures.map((procedure, i) => (
                                        <MenuItem
                                        key={`${procedure.code}-${i}`}
                                        value={procedure.id}
                                        sx={{
                                            display: "flex",
                                            gap: 1,
                                            flexDirection: "column",
                                            alignItems: "flex-start"
                                        }}
                                        >
                                        <Typography variant="subtitle1">{procedure.name}</Typography>
                                        <Typography variant="caption" color="text.secondary">
                                            {procedure.code}
                                        </Typography>
                                        </MenuItem>
                                    ))}
                                </Select>
                            </FormControl>
                         )}/>
                        )}
                    </Grid>
                    <Grid size={{xs:12, sm:6}}>
                        {disabled? (
                            <Box sx={{
                                height: "100%",
                                display: "flex",
                                flexDirection: "column",
                                gap: 1,
                                alignItems: "center",
                            }}>
                                <Typography
                                    color="textDisabled"
                                    variant="h6">
                                    Data do Procedimento
                                </Typography>
                                <Typography
                                    color="textDisabled"
                                    variant="body1">
                                    {getValues("apacData.procedureDate")}
                                </Typography>
                            </Box>
                                ):(
                            <DateProcedureSelector disabled={disabled}/>
                        )}
                    </Grid>
                </Grid>
            </Box>
        </CardForm>
    )
});

export default IdentifyMainProcedure;