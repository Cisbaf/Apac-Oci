import React from "react";
import CardForm from "@/shared/components/CardForm";
import {
  Grid,
  Typography,
  Box,
  TextField,
  Autocomplete
} from "@mui/material";
import { Controller, useWatch } from "react-hook-form";
import { useFormRequest } from "@/app/solicitar/apacRequest/contexts/FormApacRequest";
import {
  FormRepository,
  FormProps
} from "@/shared/repositories/formRepository";
import {
  MESSAGENOTCHECKVALIDITY
} from "@/app/solicitar/apacRequest/utils/messages";
import { useRequestData } from "@/app/solicitar/apacRequest/contexts/ApacRequestContext";
import { Cid } from "@/shared/schemas";

const IdentifyCidForm = React.forwardRef<FormRepository, FormProps>(
  (props, ref) => {
    const formRef = React.useRef<HTMLFormElement>(null);
    const { form, disabled: disabledForm } = useFormRequest();
    const { control, getValues } = form;
    const disabled = props.disabled ? props.disabled : disabledForm;
    const { procedures } = useRequestData();
    const procedureId = useWatch({
      control,
      name: "apacData.mainProcedureId"
    });

    const [cids, setCids] = React.useState<Cid[]>([]);

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
        if (getValues("apacData.cidId") <= 0)
          return { success: false, message: "Selecione um CID válido!" };
        return { success: true, message: "Formulário correto!" };
      }
    }));

    React.useEffect(() => {
      const procedure = procedures.find((p) => p.id === procedureId);
      if (!procedure) return;
      setCids(procedure.cid);
    }, [procedureId]);

    const getCid = () => {
      const procedure = procedures.find((p) => p.id === procedureId);
      if (!procedure) return "";
      const cidId = getValues("apacData.cidId");
      const cid = procedure.cid.find((c) => c.id === cidId);
      if (cid) return `${cid.code} - ${cid.name}`;
      return "";
    };

    return (
      <CardForm
        title="Justificativa do Procedimento"
        contentBoxStyle={{
          padding: 4
        }}
      >
        <Box ref={formRef} component="form" onSubmit={(e) => e.preventDefault()}>
          <Grid container spacing={3}>
            <Grid size={{xs:12}}>
              {disabled ? (
                <Box
                  sx={{
                    height: "100%",
                    display: "flex",
                    flexDirection: "column",
                    gap: 1,
                    justifyContent: "center"
                  }}
                >
                  <Typography color="textDisabled" variant="h6">
                    CID
                  </Typography>
                  <Typography color="textDisabled" variant="body1">
                    {getCid()}
                  </Typography>
                </Box>
              ) : (
                <Controller
                  name="apacData.cidId"
                  control={control}
                  render={({ field }) => (
                    <Autocomplete
                      options={cids}
                      getOptionLabel={(option) =>
                        `${option.code} - ${option.name}`
                      }
                      isOptionEqualToValue={(option, value) =>
                        option.id === value.id
                      }
                      value={cids.find((c) => c.id === field.value) || null}
                      onChange={(_, newValue) =>
                        field.onChange(newValue ? newValue.id : 0)
                      }
                      renderInput={(params) => (
                        <TextField
                          {...params}
                          label="CID"
                          required
                          fullWidth
                          size="medium"
                        />
                      )}
                      fullWidth
                    />
                  )}
                />
              )}
            </Grid>
          </Grid>
        </Box>
      </CardForm>
    );
  }
);

export default IdentifyCidForm;
