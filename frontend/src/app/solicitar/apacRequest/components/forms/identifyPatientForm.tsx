import React from "react";
import CardForm from "@/shared/components/CardForm";
import { TextField, Grid, Box } from "@mui/material";
import { Controller } from 'react-hook-form';
import { useFormRequest } from "@/app/solicitar/apacRequest/contexts/FormApacRequest";
import { FormRepository, FormProps } from "@/shared/repositories/formRepository";
import { useMask } from "@react-input/mask";
import { BirdDateMsk, CepMask } from "@/shared/utils/mask";
import { isValidCPF, isValidCNS } from "@/shared/utils/validate";
import { MESSAGENOTCHECKVALIDITY, MESSAGECPFINVALIDITY, MESSAGEBIRTDATEINVALIDY, MESSAGECNSINVALIDITY } from "@/app/solicitar/apacRequest/utils/messages";
import RaceColorSelector from "../field/raceColorSelector";
import GenderSelector from "../field/genderSelector";
import CpfInput from "../field/cpfInput";
import CnsInput from "../field/cnsInput";
import FormLogradouro from "../field/logradouroSelector";

const IdentifyPatientForm = React.forwardRef<FormRepository, FormProps>((props, ref)=>{
    const formRef = React.useRef<HTMLFormElement>(null); 
    const birdDateMaskRef = useMask(BirdDateMsk);
    const cepMask = useMask(CepMask);
    const { form , disabled: disabledForm } = useFormRequest();
    const { control, getValues } = form;
    const disabled = props.disabled? props.disabled : disabledForm;

    React.useImperativeHandle(ref, ()=>({
        validate(disableCheckValidate) {
            if(formRef.current && !disableCheckValidate && !formRef.current.checkValidity()){
                formRef.current.reportValidity();
                return {success: false, message: MESSAGENOTCHECKVALIDITY};
            }
            const data = getValues("apacData");
            if (!isValidCPF(data.patientCpf)) {
                return {success: false, message: MESSAGECPFINVALIDITY};
            }
            if (!isValidCNS(data.patientCns)) {
                return {success: false, message: MESSAGECNSINVALIDITY};
            }
            if (data.patientBirthDate.length != 10) {
                return {success: false, message: MESSAGEBIRTDATEINVALIDY};
            }
            return {success: true, message: "Formulário correto!"};
        },
    }));

    return(
        <CardForm
            title="Identificação do Paciente"
            contentBoxStyle={{
                padding: 4
            }}>
            <Box 
                ref={formRef} 
                component="form"
                onSubmit={(e)=>e.preventDefault()}>
                <Grid container spacing={3}>
                    <Grid size={{xs:12, sm:6}}>
                       <CnsInput formKey="patient" disabled={disabled}/>
                    </Grid>
                    <Grid size={{xs:12, sm:6}}>
                       <CpfInput disabled={disabled}/>
                    </Grid>
                    <Grid size={{xs:12, sm:8}}>
                        <Controller
                            name="apacData.patientName"
                            control={control}
                            render={({ field }) => (
                            <TextField   size="small" 
                                label="Nome Completo"
                                disabled={disabled}
                                fullWidth
                                required
                                {...field}/>
                        )}/>
                    </Grid>
                    <Grid size={{xs:12, sm:4}}>
                        <Controller
                            name="apacData.patientRecordNumber"
                            control={control}
                            render={({ field }) => (
                            <TextField   size="small" 
                                label="N° do prontuário"
                                type="number"
                                disabled={disabled}
                                fullWidth
                                {...field}/>
                            )}/>
                    </Grid>
                    <Grid size={{xs:12, sm:6, md: 3}}>
                        <Controller
                            name="apacData.patientBirthDate"
                            control={control}
                            render={({ field }) => (
                            <TextField   size="small" 
                                inputRef={birdDateMaskRef}
                                label="Data de Nascimento"
                                disabled={disabled}
                                fullWidth
                                required
                                {...field}/>
                        )}/>
                    </Grid>
                    <Grid size={{xs:12, sm:6, md: 3}}>
                        <RaceColorSelector disabled={disabled}/>
                    </Grid>
                    <Grid size={{xs:12, sm:6}}>
                        <GenderSelector disabled={disabled}/>
                    </Grid>
                    <Grid size={{xs:12, sm:6}}>
                        <Controller
                            name="apacData.patientMotherName"
                            control={control}
                            render={({ field }) => (
                            <TextField   size="small" 
                                label="Nome da mãe"
                                disabled={disabled}
                                fullWidth
                                required
                                {...field}/>
                        )}/>
                    </Grid>
                    <Grid size={{xs:12}}><hr/></Grid>
                    {/* Seção de Endereço */}
                    <Grid size={{xs:12, md:3, sm:6}}>
                        <FormLogradouro disabled={disabled}/>
                    </Grid>
                    <Grid size={{xs:12, md:3, sm:6}}>
                        <Controller
                            name="apacData.patientAddressStreetName"
                            control={control}
                            render={({ field }) => (
                            <TextField   size="small" 
                                label="Logradouro"
                                disabled={disabled}
                                fullWidth
                                required
                                {...field}/>
                        )}/>
                    </Grid>
                   
                    <Grid size={{xs:12, md:3, sm:6}}>
                        <Controller
                            name="apacData.patientAddressNumber"
                            control={control}
                            render={({ field }) => (
                            <TextField   size="small" 
                                label="Número"
                                disabled={disabled}
                                fullWidth
                                required
                                {...field}/>
                        )}/>
                    </Grid>

                    <Grid size={{xs:12, md:3, sm:6}}>
                        <Controller
                            name="apacData.patientAddressComplement"
                            control={control}
                            render={({ field }) => (
                            <TextField   size="small" 
                                label="Complemento"
                                disabled={disabled}
                                fullWidth
                                {...field}/>
                        )}/>
                    </Grid>
                    
                    <Grid size={{xs:12, md:3, sm:6}}>
                        <Controller
                            name="apacData.patientAddressPostalCode"
                            control={control}
                            render={({ field }) => (
                            <TextField   size="small" 
                                inputRef={cepMask}
                                label="CEP"
                                disabled={disabled}
                                fullWidth
                                required
                                {...field}/>
                        )}/>
                    </Grid>

                    <Grid size={{xs:12, md:3, sm:6}}>
                        <Controller
                            name="apacData.patientAddressNeighborhood"
                            control={control}
                            render={({ field }) => (
                            <TextField   size="small" 
                                label="Bairro"
                                disabled={disabled}
                                fullWidth
                                required
                                {...field}/>
                        )}/>
                    </Grid>
                    <Grid size={{xs:12, md:3, sm:6}}>
                        <Controller
                            name="apacData.patientAddressCity"
                            control={control}
                            render={({ field }) => (
                            <TextField   size="small" 
                                label="Município"
                                disabled={disabled}
                                fullWidth
                                required
                                {...field}/>
                        )}/>
                    </Grid>
                    <Grid size={{xs:12, md:3, sm:6}}>
                        <Controller
                            name="apacData.patientAddressState"
                            control={control}
                            render={({ field }) => (
                            <TextField   size="small" 
                                label="UF"
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

export default IdentifyPatientForm;