import React from "react";
import CardForm from "@/shared/components/CardForm";
import {
  Grid,
  Box,
  FormGroup,
  Typography
} from "@mui/material";
import { useFormRequest } from "../../contexts/FormApacRequest";
import { FormRepository, FormProps } from "@/shared/repositories/formRepository";
import { MESSAGENOTCHECKVALIDITY } from "@/app/solicitar/apacRequest/utils/messages";
import { useWatch } from "react-hook-form";
import { validateSubProcedures } from "./validates/validateSubProcedures";
import ProcedureItem from "./subProcedureItem";

const IdentifySubProcedures = React.forwardRef<FormRepository, FormProps>((props, ref) => {
  const formRef = React.useRef<HTMLFormElement>(null);
  const { form, disabled: disabledForm } = useFormRequest();
  const { control, register, getValues } = form;
  const subProceduresField = useWatch({
    control,
    name: "apacData.subProcedures"
  });
  const disabled = props.disabled ?? disabledForm;

  React.useImperativeHandle(ref, () => ({
    validate() {
      if (formRef.current && !formRef.current.checkValidity()) {
        formRef.current.reportValidity();
        return { success: false, message: MESSAGENOTCHECKVALIDITY };
      }

      const subProcedures = getValues("apacData.subProcedures");
      return validateSubProcedures(subProcedures);
    }
  }));


  return (
    <CardForm
      title="Procedimentos Secundários"
      contentBoxStyle={{
        padding: 4
      }}
    >
      <Box ref={formRef} component="form" onSubmit={(e) => e.preventDefault()}>
        <FormGroup>
          {subProceduresField?.length > 0 ? (
            <Grid container spacing={3}>
              {subProceduresField.map((procedure, i) =>
                !disabled || (disabled && procedure.checked) ? (
                  <ProcedureItem
                    key={`ProcedureItem-${i}`}
                    index={i}
                    procedure={procedure}
                    disabled={disabled || false}
                  />
                ) : null
              )}
            </Grid>
          ) : (
            <Typography
              variant="subtitle1"
              color="textDisabled">
                Nenhum procedimento listado!
              </Typography>
          )}
        </FormGroup>
      </Box>
    </CardForm>
  );
});

export default IdentifySubProcedures;
