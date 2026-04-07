import React from "react";
import CardForm from "@/shared/components/CardForm";
import {
  Grid,
  Autocomplete,
  TextField,
  Typography,
  Box,
  Collapse,
  Button,
  Tooltip,
  IconButton,
} from "@mui/material";
import AddCircleOutlineIcon from "@mui/icons-material/AddCircleOutline";
import HelpOutlineIcon from "@mui/icons-material/HelpOutline";

import { useFormRequest } from "@/app/solicitar/apacRequest/contexts/FormApacRequest";
import { FormRepository, FormProps } from "@/shared/repositories/formRepository";
import { explanationDateDiagnostic, MESSAGENOTCHECKVALIDITY } from "@/app/solicitar/apacRequest/utils/messages";
import { Controller, useWatch } from "react-hook-form";
import { useRequestData } from "@/app/solicitar/apacRequest/contexts/ApacRequestContext";
import DateSelector from "../field/dateSelector";
import { identifyGroup } from "../../utils/identifyGroup";
import { formatDateBr } from "../../utils/adapterForm";

const IdentifyMainProcedure = React.forwardRef<FormRepository, FormProps>(
  (props, ref) => {
    const formRef = React.useRef<HTMLFormElement>(null);
    const { form, disabled: disabledForm } = useFormRequest();
    const { control, getValues, setValue } = form;
    const { procedures } = useRequestData();
    const disabled = props.disabled ? props.disabled : disabledForm;

    const procedureId = useWatch({
      control,
      name: "apacData.mainProcedureId",
    });

    const diagnosticDate = useWatch({
      control,
      name: "apacData.diagnosticDate",
    });

    const [showDiagnosticDate, setShowDiagnosticDate] =
      React.useState(false);

    React.useImperativeHandle(ref, () => ({
      validate() {
        if (formRef.current && !formRef.current.checkValidity()) {
          formRef.current.reportValidity();
          return { success: false, message: MESSAGENOTCHECKVALIDITY };
        }
        if (getValues("apacData.mainProcedureId") <= 0)
          return {
            success: false,
            message: "Selecione um procedimento valído!",
          };
        return {
          success: true,
          message: "Formulário correto!",
        };
      },
    }));

    const getProcedure = () =>
      procedures.find((p) => p.id === procedureId);

    const getProcedureLabel = () => {
      const procedure = procedures.find((p) => p.id === procedureId);
      if (procedure) return `${procedure.code} - ${procedure.name}`;
      return "";
    };

    React.useEffect(() => {
      if (diagnosticDate && !showDiagnosticDate)
        setShowDiagnosticDate(true);
    }, [diagnosticDate]);

    return (
      <CardForm title="Procedimento Solicitado" contentBoxStyle={{ padding: 4 }}>
        <Box
          ref={formRef}
          component="form"
          onSubmit={(e) => e.preventDefault()}
        >
          <Grid container spacing={3}>
            <Grid size={{ xs: 12, sm: 6 }}>
              {disabled ? (
                <Box display={"flex"} flexDirection={"column"} gap={2}>
                  <Box display="flex" flexDirection="column" gap={1}>
                    <Typography color="textDisabled" variant="h6">
                      Procedimento
                    </Typography>
                    <Typography color="textDisabled" variant="body1">
                      {getProcedureLabel()}
                    </Typography>
                  </Box>

                  {identifyGroup(getProcedure()?.code || "") &&
                    getValues("apacData.diagnosticDate") && (
                      <Box display="flex" flexDirection="column">
                        <Typography color="textDisabled" variant="h6">
                          Data do diagnóstico
                        </Typography>
                        <Typography color="textDisabled" variant="h6">
                          {formatDateBr(
                            getValues("apacData.diagnosticDate") || ""
                          )}
                        </Typography>
                      </Box>
                    )}
                </Box>
              ) : (
                <Box display={"flex"} flexDirection={"column"}>
                  <Controller
                    name="apacData.mainProcedureId"
                    control={control}
                    render={({ field }) => (
                      <Autocomplete
                        options={procedures}
                        getOptionLabel={(option) =>
                          `${option.code} - ${option.name}`
                        }
                        isOptionEqualToValue={(option, value) =>
                          option.id === value.id
                        }
                        value={
                          procedures.find((p) => p.id === field.value) ||
                          null
                        }
                        onChange={(_, newValue) =>
                          field.onChange(newValue ? newValue.id : 0)
                        }
                        renderInput={(params) => (
                          <TextField
                            {...params}
                            label="Procedimento Principal"
                            required
                            fullWidth
                          />
                        )}
                        fullWidth
                        disabled={disabled}
                      />
                    )}
                  />

                  {identifyGroup(getProcedure()?.code || "") && (
                    <>
                      {/* BOTÃO + HELP (CORRIGIDO) */}
                      <Collapse in={!showDiagnosticDate}>
                        <Box
                          display="flex"
                          alignItems="center"
                          mt={1}
                        >
                          <Button
                            size="small"
                            startIcon={<AddCircleOutlineIcon />}
                            onClick={() =>
                              setShowDiagnosticDate(true)
                            }
                            sx={{ textTransform: "none" }}
                            disabled={disabled}
                          >
                            Informar data diagnóstico
                          </Button>

                          <Tooltip title={explanationDateDiagnostic}>
                            <IconButton size="small">
                              <HelpOutlineIcon fontSize="small" />
                            </IconButton>
                          </Tooltip>
                        </Box>
                      </Collapse>

                      {/* CAMPO */}
                      <Collapse in={showDiagnosticDate}>
                        <Box
                          mt={2}
                          display="flex"
                          flexDirection="column"
                          gap={1}
                        >
                          <Controller
                            name="apacData.diagnosticDate"
                            control={control}
                            render={({ field }) => (
                              <TextField
                                {...field}
                                type="date"
                                label="Data do diagnóstico"
                                fullWidth
                                InputLabelProps={{ shrink: true }}
                              />
                            )}
                          />

                          <Button
                            size="small"
                            color="error"
                            onClick={() => {
                              setValue(
                                "apacData.diagnosticDate",
                                ""
                              );
                              setShowDiagnosticDate(false);
                            }}
                            sx={{
                              textTransform: "none",
                              alignSelf: "flex-start",
                            }}
                          >
                            Remover data
                          </Button>
                        </Box>
                      </Collapse>
                    </>
                  )}
                </Box>
              )}
            </Grid>

            <Grid size={{ xs: 12, sm: 6, md: 3 }}>
              {disabled ? (
                <Box display="flex" flexDirection="column" alignItems="center">
                  <Typography color="textDisabled" variant="h6">
                    Data do Procedimento
                  </Typography>
                  <Typography color="textDisabled">
                    {getValues("apacData.procedureDate")}
                  </Typography>
                </Box>
              ) : (
                <DateSelector formKey="procedure" disabled={disabled} />
              )}
            </Grid>

            <Grid size={{ xs: 12, sm: 6, md: 3 }}>
              {disabled ? (
                <Box display="flex" flexDirection="column" alignItems="center">
                  <Typography color="textDisabled" variant="h6">
                    Data da Alta
                  </Typography>
                  <Typography color="textDisabled">
                    {getValues("apacData.dischargeDate")}
                  </Typography>
                </Box>
              ) : (
                <DateSelector formKey="discharge" disabled={disabled} />
              )}
            </Grid>
          </Grid>
        </Box>
      </CardForm>
    );
  }
);

export default IdentifyMainProcedure;