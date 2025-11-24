export function GenerateStringToDownloadFile(filename: string, content: string) {
    filename = filename.replace(/\.+$/, ""); // remove pontos no final

    const contentWindows = content.replace(/\n/g, "\r\n");
    const blob = new Blob([contentWindows], { type: "application/octet-stream" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");

    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();

    a.remove();
    window.URL.revokeObjectURL(url);
}
