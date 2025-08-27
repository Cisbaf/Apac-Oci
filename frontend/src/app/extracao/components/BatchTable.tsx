import React from "react";
import {
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow,
  Checkbox, Paper,
  Button,
  Box
} from "@mui/material";
import { useExportContext } from "../contexts/ExportContext";
import { formatDateBr } from "@/app/solicitar/apacRequest/utils/adapterForm";


export default function BatchTable() {
  const { hookBatchsList, hookExtractForm, extract } = useExportContext();

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell padding="checkbox">
              <Checkbox
                indeterminate={
                  hookExtractForm.batchsSelected.length > 0 &&
                  hookExtractForm.batchsSelected.length < hookBatchsList.batchs.length
                }
                checked={hookExtractForm.batchsSelected.length === hookBatchsList.batchs.length}
                onChange={(e) =>
                  e.target.checked ?
                  hookBatchsList.batchs.forEach(b=>hookExtractForm.addBatchId(b.id)):
                  hookBatchsList.batchs.forEach(b=>hookExtractForm.removeBatchId(b.id))
                }
              />
            </TableCell>
            <TableCell>Paciente</TableCell>
            <TableCell>Procedimento</TableCell>
            <TableCell>Cid</TableCell>
            <TableCell>Data do Procedimento</TableCell>
            <TableCell>Faixa Apac</TableCell>
            <TableCell>Detalhes</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {hookBatchsList.batchs.map((row) => (
            <TableRow key={row.id}>
              <TableCell padding="checkbox">
                <Checkbox
                  checked={hookExtractForm.batchsSelected.includes(row.id)}
                  onChange={() => 
                    hookExtractForm.batchsSelected.includes(row.id)?
                    hookExtractForm.removeBatchId(row.id):
                    hookExtractForm.addBatchId(row.id)}/>
              </TableCell>
                <TableCell>{row.apac_request.apac_data.patient_data.name}</TableCell>
                <TableCell>{row.apac_request.apac_data.main_procedure.name}</TableCell>
                <TableCell>{`${row.apac_request.apac_data.cid.code} - ${row.apac_request.apac_data.cid.name}`}</TableCell>
                <TableCell>{formatDateBr(row.apac_request.apac_data.procedure_date)}</TableCell>
                <TableCell>{row.batch_number}</TableCell>
                <TableCell>...</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <Box sx={{
          display: "flex",
          justifyContent: "end"
      }}>
          <Button 
            sx={{margin: 2}}
            variant="contained"
            onClick={extract}>Extrair</Button>
      </Box>
    </TableContainer>
  );
}
