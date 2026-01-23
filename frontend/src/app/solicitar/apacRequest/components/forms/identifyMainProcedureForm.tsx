import React from "react";
import CardForm from "@/shared/components/CardForm";
import { Grid, Autocomplete, TextField, Typography, Box } from "@mui/material";
import { useFormRequest } from "@/app/solicitar/apacRequest/contexts/FormApacRequest";
import { FormRepository, FormProps } from "@/shared/repositories/formRepository";
import { MESSAGENOTCHECKVALIDITY } from "@/app/solicitar/apacRequest/utils/messages";
import { Controller, useWatch } from 'react-hook-form';
import { useRequestData } from "@/app/solicitar/apacRequest/contexts/ApacRequestContext";
import DateSelector from "../field/dateSelector";

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
            contentBoxStyle={{ padding: 4}}>
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
                            <Autocomplete
                            options={procedures}
                            getOptionLabel={(option) => `${option.code} - ${option.name}`}
                            isOptionEqualToValue={(option, value) => option.id === value.id}
                            value={procedures.find((p) => p.id === field.value) || null}
                            onChange={(_, newValue) =>
                                field.onChange(newValue ? newValue.id : 0)
                            }
                            renderInput={(params) => (
                                <TextField
                                {...params}
                                label="Procedimento Principal"
                                required
                                fullWidth
                                size="medium"
                                />
                            )}
                            renderOption={(props, option) => (
                                <li
                                {...props}
                                key={option.id}
                                style={{
                                    display: "flex",
                                    flexDirection: "column",
                                    alignItems: "flex-start",
                                    padding: "8px 12px",
                                    borderBottom: "1px solid #f0f0f0",
                                }}
                                >
                                <Typography
                                    variant="body1"
                                    key={`tp-${option.id}`}
                                    sx={{
                                    fontWeight: 500,
                                    whiteSpace: "normal",
                                    lineHeight: 1.4,
                                    color: "#333",
                                    }}
                                >
                                    {option.name}
                                </Typography>
                                <Typography
                                    key={`tp2-${option.id}`}
                                    variant="body2"
                                    sx={{
                                    color: "#777",
                                    fontFamily: "monospace",
                                    marginTop: "2px",
                                    fontSize: "0.8rem",
                                    }}
                                >
                                    Código: {option.code}
                                </Typography>
                                </li>
                            )}
                            fullWidth
                            disabled={disabled}
                            ListboxProps={{
                                style: {
                                maxHeight: 300,
                                padding: 0,
                                borderRadius: 8,
                                boxShadow: "0 4px 10px rgba(0,0,0,0.1)",
                                },
                            }}
                            />
                        )}
                        />
                        )}
                    </Grid>
                    <Grid size={{xs:12, sm:6, md: 3}}>
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
                            <DateSelector formKey="procedure" disabled={disabled}/>
                        )}
                    </Grid>
                    <Grid size={{xs:12, sm:6, md: 3}}>
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
                                    Data da Alta
                                </Typography>
                                <Typography
                                    color="textDisabled"
                                    variant="body1">
                                    {getValues("apacData.dischargeDate")}
                                </Typography>
                            </Box>
                                ):(
                            <DateSelector formKey="discharge" disabled={disabled}/>
                        )}
                    </Grid>

                </Grid>
            </Box>
        </CardForm>
    )
});

export default IdentifyMainProcedure;