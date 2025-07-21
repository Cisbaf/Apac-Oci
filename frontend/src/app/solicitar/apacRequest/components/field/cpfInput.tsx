import { Controller } from 'react-hook-form';
import { useFormRequest } from "@/app/solicitar/apacRequest/contexts/FormApacRequest";
import { TextField, IconButton, InputAdornment } from '@mui/material';
import { Search as SearchIcon } from '@mui/icons-material';
import { CpfMask } from "@/shared/utils/mask";
import { useMask } from "@react-input/mask";
import { isValidCPF } from "@/shared/utils/validate";
import { useGlobalComponents } from '@/shared/context/GlobalUIContext';
import { fillRequestFormFromPatient } from '../../services/PatientInfoService';


export default function CpfInput( props : { disabled?: boolean }) {
    const { form } = useFormRequest();
    const { control, setValue } = form;
    const cpfMaskRef = useMask(CpfMask);
    const { showBackdrop, showResponseApi, showAlert } = useGlobalComponents();

    const handleSearchClick = async() => {
        const cpf = cpfMaskRef.current?.value;
        if (cpf && isValidCPF(cpf)) {
            showBackdrop(true, "Buscando dados...");
            try {
                const response = await fetch("/api/cadsus",{
                    method: "POST",
                    body: JSON.stringify({
                        type_consult: "cpf",
                        value: cpf
                    })
                })
                
                const response_json = await showResponseApi(response);
                fillRequestFormFromPatient(response_json, setValue);
            } catch (e) {
                showAlert({ color: "error", message: "Erro ao tentar preencher dados automáticos, por favor preencha manualmente!"})
            }

            showBackdrop(false);
        } else {
            showAlert({color: "error", message: "CPF invalido"});
        }
    };

    return (
        <Controller
            name="apacData.patientCpf"
            control={control}
            render={({ field }) => (
                <TextField
                    size="small"
                    inputRef={cpfMaskRef}
                    label="CPF do paciente"
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
                                    aria-label="Pesquisar CPF"
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
