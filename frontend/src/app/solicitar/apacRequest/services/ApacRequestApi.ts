import { DataApacRequest } from "../contexts/ApacRequestContext";

export function ApacRequestFetchApi(): Promise<DataApacRequest> {
    return new Promise(async(resolve, reject)=>{
        const endpoints = {
            establishments: '/api/proxy/establishment/apac',
            procedures: '/api/proxy/procedure/apac',
        };
          try {
            const entries = await Promise.all(
              Object.entries(endpoints).map(async ([key, url]) => {
                const res = await fetch(url);
        
                if (!res.ok) throw new Error(`Erro ao buscar ${key}: ${res.statusText}`);
                const json = await res.json();
                return [key, json];
              })
            );
        
            const result = Object.fromEntries(entries);
            resolve(result);
          } catch (error) {
            console.error('Erro ao buscar dados:', error);
            reject('Erro ao buscar dados');
          }
    });
}