import { Establishment } from "@/shared/schemas";

export function GetEstablishments(): Promise<Establishment[]> {
    return new Promise(async (resolve, reject)=>{
        try {
            const request = await fetch("/api/proxy/establishment/apac");
            if (!request.ok) return reject(await request.json());
            return resolve(request.json());
        } catch(e) {
            reject(e);
        }
    });

}