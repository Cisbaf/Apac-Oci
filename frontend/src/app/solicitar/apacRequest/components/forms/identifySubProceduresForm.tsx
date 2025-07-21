import React from "react";
import CardForm from "@/shared/components/CardForm";
import {
  Grid,
  Box,
  TextField,
  FormGroup,
  FormControlLabel,
  Checkbox,
  Typography
} from "@mui/material";
import { useFormRequest } from "../../contexts/FormApacRequest";
import { FormRepository, FormProps } from "@/shared/repositories/formRepository";
import { MESSAGENOTCHECKVALIDITY } from "@/app/solicitar/apacRequest/utils/messages";
import { Controller, useWatch } from "react-hook-form";
import { SubProceduresForm } from "@/app/solicitar/apacRequest/schemas/requestForm";

type ProcedureItemProps = {
  i: number;
  control: any;
  register: any;
  subProcedure: SubProceduresForm;
  disabled: boolean;
};


function ProcedureItem({ i, control, register, subProcedure, disabled }: ProcedureItemProps) {
  return (
    <Grid size={{xs:12}}>
      <Box display="flex" alignItems="center">
        <FormControlLabel
          sx={{ flex: 1 }}
          control={
            <Controller
              control={control}
              name={`apacData.subProcedures.${i}.checked`}
              defaultValue={subProcedure.checked}
              render={({ field }) => (
                <Checkbox {...field} checked={field.value} required={subProcedure.procedure.mandatory} disabled={disabled} />
              )}
            />
          }
          label={
            <Typography
              color={(disabled? "textDisabled" : subProcedure.procedure.mandatory && "primary") || ""}>
              {`${subProcedure.procedure.name}`}
            </Typography>}
        /> 
        <TextField   size="small" 
          label="Quantidade"
          type="number"
          disabled={disabled || !subProcedure.checked}
          sx={{ flex: 0.3 }}
          {...register(`apacData.subProcedures.${i}.quantity`)}
        />
      </Box>
    </Grid>
  );
}

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
        return {
          success: false,
          message: MESSAGENOTCHECKVALIDITY
        };
      }

      const subProcedures = getValues("apacData.subProcedures");

      const mandatorys_not_checked = subProcedures.find(p=>p.procedure.mandatory && !p.checked);

      if (mandatorys_not_checked) {
        return {
          success: false,
          message: `O procedimento obrigatório ${mandatorys_not_checked.procedure.name} não foi selecionado!`
        };
      }

      const incorrect = subProcedures.find(
        (p) => p.checked && (!p.quantity || p.quantity <= 0)
      );

      if (incorrect) {
        return {
          success: false,
          message: `Defina a quantidade para o procedimento ${incorrect.procedure.name}`
        };
      }

      return {
        success: true,
        message: "ok"
      };
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
                    i={i}
                    control={control}
                    register={register}
                    subProcedure={procedure}
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
