import { Controller } from 'react-hook-form';
import { useFormRequest } from "@/app/solicitar/apacRequest/contexts/FormApacRequest";
import { TextField, IconButton, InputAdornment } from '@mui/material';
import { Search as SearchIcon } from '@mui/icons-material';
import { CnsMask } from "@/shared/utils/mask";
import { useMask } from "@react-input/mask";
import { useGlobalComponents } from '@/shared/context/GlobalUIContext';
import { fillRequestFormFromPatient } from '../../services/PatientInfoService';

interface CnsInputProps {
    formKey: "patient"|"supervising"|"authorizing";
    disabled?: boolean;
}

export default function CnsInput(props: CnsInputProps) {
    const { form } = useFormRequest();
    const { control, setValue } = form;
    const cnsMaskRef = useMask(CnsMask);
    const { showBackdrop, showResponseApi, showAlert } = useGlobalComponents();
    const chv = {
        patient: {form: "apacData.patientCns", label: "Cns do paciente"},
        supervising: {form: "apacData.supervisingPhysicianCns", label: "Cns do medico responsavel"},
        authorizing: {form: "apacData.authorizingPhysicianCns", label: "Cns do medico autorizador"},
    } as const;

    const handleSearchClick = async() => {
        const cns = cnsMaskRef.current?.value.replace(/\s+/g, '');
        if (cns && cns.length === 15) {
            showBackdrop(true, "Buscando dados...");
            try {
                const response = await fetch("/api/cadsus",{
                    method: "POST",
                    body: JSON.stringify({
                        type_consult: "cns",
                        value: cns
                    })
                })
                const patient_info = await showResponseApi(response);
                if (response.ok && props.formKey == "patient") {
                    fillRequestFormFromPatient(patient_info, setValue);
                } else if (response.ok && props.formKey == "supervising") {
                    setValue("apacData.supervisingPhysicianName", patient_info.full_name);
                } else if (response.ok && props.formKey == "authorizing") {
                    setValue("apacData.authorizingPhysicianName", patient_info.full_name);
                }
                
            } catch (e) {
                showAlert({ color: "error", message: "Erro ao tentar preencher dados automáticos, por favor preencha manualmente!"})
            }

            showBackdrop(false);
        } else {
            showAlert({color: "error", message: "CNS invalido"});
        }
    };

    return (
        <Controller
            name={chv[props.formKey].form}
            control={control}
            render={({ field }) => (
                <TextField
                    size="small"
                    inputRef={cnsMaskRef}
                    label={chv[props.formKey].label}
                    disabled={props.disabled}
                    required
                    fullWidth
                    {...field}
                    InputProps={{
                        endAdornment: (
                            <InputAdornment position="end">
                                <IconButton
                                    onClick={handleSearchClick}
                                    edge="end"
                                    disabled={props.disabled}
                                    aria-label="Pesquisar"
                                >
                                    <SearchIcon />
                                </IconButton>
                            </InputAdornment>
                        ),
                    }}
                />
            )}
        />
    );
}
