import City from "./city";

export default interface Establishment {
    id: number;
    name: string;
    cnes: string;
    city: City;
    is_active: boolean;
  }