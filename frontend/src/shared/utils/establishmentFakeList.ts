import { Establishment } from "../schemas";


export const establishmentFakeList: Establishment[] = [
     {
        id: 1,
        name: "Hospital Municipal São Lucas",
        cnes: "1234567",
        city: {
          id: 1,
          name: "Rio de Janeiro"
        },
        is_active: true
      },
      {
        id: 2,
        name: "Hospital Geral de Jacarepaguá",
        cnes: "7654321",
        city: {
          id: 1,
          name: "Rio de Janeiro"
        },
        is_active: true
      },
      {
        id: 3,
        name: "Hospital Universitário Clementino Fraga Filho",
        cnes: "9876543",
        city: {
          id: 2,
          name: "São Paulo"
        },
        is_active: true
      }
] 