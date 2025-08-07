import { SubProceduresForm } from "../schemas/requestForm";


export function adapterFormSubProcedures(subProcedures: SubProceduresForm[]): unknown {
    const sub_checkeds = subProcedures.filter(p=>p.checked);
    return sub_checkeds.map(p=>{
         return {
            procedure_id: p.procedure.id,
            quantity: p.quantity
        } 
    })
}

export function formatDateToISO(dateStr: string) {
  const [day, month, year] = dateStr.split('/');
  return `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
}

export function formatDateBr(dateString: string) {
  const [year, month, day] = dateString.split('-');
  return `${day}/${month}/${year}`;
}