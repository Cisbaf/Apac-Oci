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