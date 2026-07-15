import React from "react";
import {
  TextField,
  Autocomplete
} from "@mui/material";
import { Controller } from "react-hook-form";
import { useFormRequest } from "@/app/solicitar/apacRequest/contexts/FormApacRequest";
import {
  FormRepository,
  FormProps
} from "@/shared/repositories/formRepository";
import {
  MESSAGENOTCHECKVALIDITY
} from "@/app/solicitar/apacRequest/utils/messages";

import { LOGRADOUROS } from "../../utils/logradouros";



const FormLogradouro = React.forwardRef<FormRepository, FormProps>(
  (props, ref) => {
    const formRef = React.useRef<HTMLFormElement>(null);
    const { form } = useFormRequest();
    const { control, getValues } = form;

    React.useImperativeHandle(ref, () => ({
      validate(disableCheckValidate) {
        if (
          formRef.current &&
          !disableCheckValidate &&
          !formRef.current.checkValidity()
        ) {
          formRef.current.reportValidity();
          return { success: false, message: MESSAGENOTCHECKVALIDITY };
        }
        if (!getValues("apacData.patientAddressStreetType"))
          return { success: false, message: "Selecione um tipo de logradouro!" };
        return { success: true, message: "Formulário correto!" };
      }
    }));

    return (
        <Controller
            name="apacData.patientAddressStreetType"
            control={control}
            render={({ field }) => (
            <Autocomplete
                disabled={props.disabled}
                options={LOGRADOUROS}
                getOptionLabel={(option) =>
                `${option.code} - ${option.name}`
                }
                isOptionEqualToValue={(option, value) =>
                option.code === value.code
                }
                value={
                LOGRADOUROS.find((l) => l.code === field.value) || null
                }
                onChange={(_, newValue) =>
                field.onChange(newValue ? newValue.code : "")
                }
                renderInput={(params) => (
                <TextField
                    {...params}
                    label="Tipo de Logradouro"
                    required
                    fullWidth
                />
                )}
                fullWidth
            />
            )}
        />
    );
  }
);

FormLogradouro.displayName = "FormLogradouro";

export default FormLogradouro;
