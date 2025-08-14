

export function getFirstDays(monthCount: number): Date[] {
    const today = new Date();
    const dates: Date[] = [];

    for (let i = 0; i < monthCount; i++) {
        // Primeiro dia do mês atual menos i meses
        const date = new Date(today.getFullYear(), today.getMonth() - i, 1);
        dates.push(date);
    }

    return dates;
}

export function getMonthNamePtBr(dateInput: string | Date): string {
    const date = typeof dateInput === "string" ? new Date(dateInput) : dateInput;
    return date.toLocaleDateString("pt-BR", { month: "long", year: "numeric" });
}

export function formatDateToYMD(date: Date): string {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0"); // +1 porque mês começa em 0
    const day = String(date.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
}