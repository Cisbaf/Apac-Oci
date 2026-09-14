import React from "react";
import CardForm from "@/shared/components/CardForm";
import {
  Grid,
  Box,
  FormGroup,
  Typography,
  Alert
} from "@mui/material";
import { useFormRequest } from "../../contexts/FormApacRequest";
import { useRequestData } from "../../contexts/ApacRequestContext";
import { FormRepository, FormProps } from "@/shared/repositories/formRepository";
import { MESSAGENOTCHECKVALIDITY } from "@/app/solicitar/apacRequest/utils/messages";
import { useWatch } from "react-hook-form";
import { validatePmae, validateSubProcedures } from "./validates/validateSubProcedures";
import ProcedureItem from "./subProcedureItem";

const IdentifySubProcedures = React.forwardRef<FormRepository, FormProps>((props, ref) => {
  const formRef = React.useRef<HTMLFormElement>(null);
  const { form, disabled: disabledForm } = useFormRequest();
  const { control, getValues } = form;
  const { procedures } = useRequestData();
  const subProceduresField = useWatch({
    control,
    name: "apacData.subProcedures"
  });
  const mainProcedureId = useWatch({
    control,
    name: "apacData.mainProcedureId"
  });
  const disabled = props.disabled ?? disabledForm;

  // "Exige ao menos N destes M" (atributos SIGTAP 057/067-070, T-040) e a regra
  // PMAE (atributo 053, T-043) vêm do procedimento principal, não do
  // secundário; por isso não estão em `procedure` de cada item da lista.
  const mainProcedure = procedures.find(p => p.id === mainProcedureId);
  const requirementGroups = mainProcedure?.requirement_groups ?? [];
  const avisoPmae = validatePmae(
    (subProceduresField ?? []).filter(p => p.checked),
    mainProcedure
  );

  React.useImperativeHandle(ref, () => ({
    validate() {
      if (formRef.current && !formRef.current.checkValidity()) {
        formRef.current.reportValidity();
        return { success: false, message: MESSAGENOTCHECKVALIDITY };
      }

      const subProcedures = getValues("apacData.subProcedures");
      return validateSubProcedures(subProcedures, requirementGroups, mainProcedure);
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
        {!disabled && mainProcedure?.pmae && (
          <Alert severity={avisoPmae ? "warning" : "success"} sx={{ mb: 2 }}>
            {avisoPmae ??
              "Mínimo de procedimentos secundários da OCI atendido, com consulta ou teleconsulta."}
          </Alert>
        )}
        {!disabled && requirementGroups.map(group => {
          const marcados = (subProceduresField ?? []).filter(
            p => p.checked && group.member_ids.includes(p.procedure.id)
          ).length;
          const satisfeito = marcados >= group.minimum;
          return (
            <Alert key={group.id} severity={satisfeito ? "success" : "warning"} sx={{ mb: 2 }}>
              Este procedimento exige pelo menos {group.minimum} de: {group.description}
              {satisfeito ? " — selecionado." : " — ainda não selecionado."}
            </Alert>
          );
        })}
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

IdentifySubProcedures.displayName = "IdentifySubProcedures";

export default IdentifySubProcedures;
