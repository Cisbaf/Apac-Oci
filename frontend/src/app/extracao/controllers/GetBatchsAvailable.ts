import { ApacBatch } from "../schemas/apacBatch";
import { ExtractFormData } from "../schemas/extractForm";

export async function GetBatchsAvailable(data: ExtractFormData): Promise<ApacBatch[]> {
  
  const month = data.production.getMonth() + 1;
  const year = data.production.getFullYear();

  try {
      const response = await fetch(
        `/api/proxy/apac_batch/availables?establishment_id=${data.establishmentId}&competence_month=${month}&competence_year=${year}`
      );

      if (!response.ok) {
        throw new Error(`Erro na requisição: ${response.statusText}`);
      }

      return (await response.json()) as ApacBatch[];
  } catch (err) {
      console.error("Erro ao buscar batches:", err);
      throw err;
  }
}
