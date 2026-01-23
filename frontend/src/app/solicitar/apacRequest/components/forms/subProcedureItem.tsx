import React, { useEffect } from "react";
import {
  Grid,
  Box,
  TextField,
  FormControlLabel,
  Checkbox,
  Typography,
  Collapse,
  Button,
  Paper,
  IconButton
} from "@mui/material";
import AddCircleOutlineIcon from "@mui/icons-material/AddCircleOutline";
import CloseIcon from "@mui/icons-material/Close";
import { Controller, useWatch } from "react-hook-form";
import { SubProceduresForm } from "@/app/solicitar/apacRequest/schemas/requestForm";
import { useFormRequest } from "../../contexts/FormApacRequest";

type ProcedureItemProps = {
  index: number;
  procedure: SubProceduresForm;
  disabled: boolean;
};

export default function ProcedureItem({
  index,
  procedure,
  disabled
}: ProcedureItemProps) {
  const { form } = useFormRequest();
  const { control, setValue, register } = form;

  const isChecked = useWatch({
    control,
    name: `apacData.subProcedures.${index}.checked`
  });

  const useThirdParty = useWatch({
    control,
    name: `apacData.subProcedures.${index}.useThirdPartyData`
  });

  const isMandatory = procedure.procedure.mandatory;

  // Limpa CBO/CNES se desativar
  useEffect(() => {
    if (!useThirdParty) {
      setValue(`apacData.subProcedures.${index}.cbo`, "");
      setValue(`apacData.subProcedures.${index}.cnes`, "");
    }
  }, [useThirdParty, setValue, index]);

  return (
    <Grid container spacing={1} sx={{ mb: 1.5 }}>
      {/* Linha principal */}
      <Grid size={{ xs: 12 }}>
        <Box
          display="flex"
          alignItems="center"
          justifyContent="space-between"
          gap={2}
          flexWrap="wrap"
        >
          <FormControlLabel
            sx={{ flex: 1, minWidth: 260, m: 0 }}
            control={
              <Controller
                control={control}
                name={`apacData.subProcedures.${index}.checked`}
                defaultValue={procedure.checked}
                render={({ field }) => (
                  <Checkbox
                    {...field}
                    checked={field.value}
                    required={isMandatory}
                    disabled={disabled}
                  />
                )}
              />
            }
            label={
              <Typography color={ disabled ? "textDisabled" : isMandatory ? "primary" : undefined }>
                {procedure.procedure.name}
              </Typography>
            }
          />

          <TextField
            size="small"
            label="Qtd."
            type="number"
            sx={{ width: 90 }}
            disabled={disabled || !isChecked}
            {...register(`apacData.subProcedures.${index}.quantity`)}
          />
        </Box>
      </Grid>

      {!disabled && (
        <Grid size={{ xs: 12 }}>
          {/* Ação discreta para CBO/CNES */}
          <Collapse in={isChecked && !useThirdParty}>
            <Button
              size="small"
              startIcon={<AddCircleOutlineIcon />}
              onClick={() =>
                setValue(
                  `apacData.subProcedures.${index}.useThirdPartyData`,
                  true
                )
              }
              sx={{ textTransform: "none", mt: 0.5, ml: 4 }}
              disabled={disabled}
            >
              Informar CBO/CNES de outro profissional / estabelecimento
            </Button>
          </Collapse>
        </Grid>
      )}
  

      {/* Bloco leve com CBO e CNES */}
      <Grid size={{ xs: 12 }}>
        <Collapse in={isChecked && useThirdParty}>
          <Paper
            variant="outlined"
            sx={{
              p: 2,
              mt: 1,
              ml: 4,
              borderRadius: 2,
              backgroundColor: "grey.50"
            }}
          >
            <Box
              display="flex"
              justifyContent="space-between"
              alignItems="center"
              mb={1}
            >
              <Typography variant="caption" color="text.secondary">
                Dados do profissional / estabelecimento executante
              </Typography>

              {!disabled && (
                <IconButton
                size="small"
                onClick={() =>
                  setValue(
                    `apacData.subProcedures.${index}.useThirdPartyData`,
                    false
                  )
                }
              >
                <CloseIcon fontSize="small" />
              </IconButton>
              )}
            </Box>

            <Grid container spacing={2}>
              <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                <TextField
                  size="small"
                  label="CBO"
                  type="number"
                  fullWidth
                  disabled={disabled}
                  {...register(`apacData.subProcedures.${index}.cbo`)}
                />
              </Grid>

              <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                <TextField
                  size="small"
                  label="CNES"
                  type="number"
                  fullWidth
                  disabled={disabled}
                  {...register(`apacData.subProcedures.${index}.cnes`)}
                />
              </Grid>
            </Grid>
          </Paper>
        </Collapse>
      </Grid>
    </Grid>
  );
}
