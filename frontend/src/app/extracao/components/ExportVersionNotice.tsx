"use client";
import { useState } from "react";
import { Alert, AlertTitle, Collapse } from "@mui/material";

export default function ExportVersionNotice() {
    const [open, setOpen] = useState(true);

    return (
        <Collapse in={open}>
            <Alert severity="warning" onClose={() => setOpen(false)}>
                <AlertTitle>Atenção: novos campos no arquivo exportado</AlertTitle>
                Desde a competência 07/2026, o arquivo gerado passa a incluir os campos
                exigidos pelas versões mais recentes do APAC Magnético: &quot;Pessoa sem
                CPF/Registro Civil&quot; (v04.00) e &quot;Fonte Orçamentária&quot;/&quot;Recurso
                de Emendas Parlamentares&quot; (v03.17). Antes de importar, confirme que o
                APAC Magnético instalado no seu computador está atualizado para a versão
                mais recente (disponível em{" "}
                <a href="https://sia.datasus.gov.br" target="_blank" rel="noopener noreferrer">
                    sia.datasus.gov.br
                </a>
                ). Uma versão desatualizada pode rejeitar a importação ou não reconhecer os
                campos novos.
            </Alert>
        </Collapse>
    );
}
