
export function GenerateStringToDownloadFile(filename: string, content: string) {
    // Prefixo BOM
    const bom = '\uFEFF';
    const blob = new Blob([bom + content], { type: "text/plain;charset=utf-8" });

    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();

    a.remove();
    window.URL.revokeObjectURL(url);
}
