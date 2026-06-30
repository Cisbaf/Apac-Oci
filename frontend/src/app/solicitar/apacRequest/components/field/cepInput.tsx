import { Controller } from 'react-hook-form';
import { useFormRequest } from "@/app/solicitar/apacRequest/contexts/FormApacRequest";
import { TextField, IconButton, InputAdornment } from '@mui/material';
import { Search as SearchIcon } from '@mui/icons-material';
import { CepMask } from "@/shared/utils/mask";
import { useMask } from "@react-input/mask";
import { useGlobalComponents } from '@/shared/context/GlobalUIContext';

export default function CepInput(props: { disabled?: boolean }) {
    const { form } = useFormRequest();
    const { control, setValue } = form;
    const cepMaskRef = useMask(CepMask);
    const { showBackdrop, showAlert } = useGlobalComponents();

    const handleSearchClick = async () => {
        const cep = cepMaskRef.current?.value.replace(/\D/g, '');
        if (!cep || cep.length !== 8) {
            showAlert({ color: "error", message: "CEP inválido" });
            return;
        }

        showBackdrop(true, "Buscando endereço...");
        try {
            const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
            const data = await response.json();

            if (data.erro) {
                showAlert({ color: "error", message: "CEP não encontrado" });
            } else {
                setValue('apacData.patientAddressStreetName', data.logradouro || '');
                setValue('apacData.patientAddressNeighborhood', data.bairro || '');
                setValue('apacData.patientAddressCity', data.localidade || '');
                setValue('apacData.patientAddressState', data.uf || '');
            }
        } catch {
            showAlert({ color: "error", message: "Erro ao buscar CEP, verifique sua conexão" });
        }

        showBackdrop(false);
    };

    return (
        <Controller
            name="apacData.patientAddressPostalCode"
            control={control}
            render={({ field }) => (
                <TextField
                    size="small"
                    inputRef={cepMaskRef}
                    label="CEP"
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
                                    aria-label="Buscar CEP"
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
