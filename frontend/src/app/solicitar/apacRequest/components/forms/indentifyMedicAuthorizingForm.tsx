import React from "react";
import CardForm from "@/shared/components/CardForm";
import { TextField, Grid, Box } from "@mui/material";
import { Controller } from 'react-hook-form';
import { useFormRequest } from "@/app/solicitar/apacRequest/contexts/FormApacRequest";
import { FormRepository, FormProps } from "@/shared/repositories/formRepository";
import { MESSAGENOTCHECKVALIDITY,} from "@/app/solicitar/apacRequest/utils/messages";
import { isValidCNS } from "@/shared/utils/validate";
import CnsInput from "../field/cnsInput";

const IdentifyMedicAuthorizingForm = React.forwardRef<FormRepository, FormProps>((props, ref)=>{
    const formRef = React.useRef<HTMLFormElement>(null); 
    const { form , disabled: disabledForm } = useFormRequest();
    const { control } = form;
    const disabled = props.disabled? props.disabled : disabledForm;

    React.useImperativeHandle(ref, ()=>({
        validate(disableCheckValidate) {
            if(formRef.current && !disableCheckValidate && !formRef.current.checkValidity()){
                formRef.current.reportValidity();
                return {success: false, message: MESSAGENOTCHECKVALIDITY};
            }
            return {success: true, message: "Formulário correto!"};
        },
    }));

    return(
        <CardForm
            title="Medico Autorizador"
            contentBoxStyle={{
                padding: 4
            }}>
            <Box 
                ref={formRef} 
                component="form"
                onSubmit={(e)=>e.preventDefault()}>
                <Grid container spacing={3}>
                    <Grid size={{xs:12, sm:12}}>
                        <Controller
                            name="apacData.authorizingPhysicianName"
                            control={control}
                            render={({ field }) => (
                            <TextField   size="small" 
                                label="Nome do Profissional"
                                disabled={disabled}
                                fullWidth
                                required
                                {...field}/>
                        )}/>
                    </Grid>
                    <Grid size={{xs:12, sm:6}}>
                       <CnsInput formKey="authorizing" disabled={disabled}/>
                    </Grid>
                    <Grid size={{xs:12, sm:6}}>
                        <Controller
                            name="apacData.authorizingPhysicianCbo"
                            control={control}
                            render={({ field }) => (
                            <TextField   size="small" 
                                label="CBO do Profissional"
                                disabled={disabled}
                                fullWidth
                                required
                                {...field}/>
                        )}/>
                    </Grid>
                </Grid>
            </Box>
        </CardForm>
    )
});

export default IdentifyMedicAuthorizingForm;