
export function GenerateStringToDownloadFile(filename: string, content: string) {
        const blob = new Blob([content], { type: "text/plain" });

        // gera uma URL temporária
        const url = window.URL.createObjectURL(blob);

        // cria um link "invisível"
        const a = document.createElement("a");
        a.href = url;
        a.download = filename; // nome do arquivo
        document.body.appendChild(a);
        a.click();

        // limpa recursos
        a.remove();
        window.URL.revokeObjectURL(url);
}