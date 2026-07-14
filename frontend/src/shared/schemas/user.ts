import City from "./city";

export enum UserRole {
  ADMIN = "admin",
  REQUESTER = "requester",
  AUTHORIZER = "authorizer",
  GUEST = "guest"
}

export default interface User {
  id: number;
  name: string;
  role: UserRole;
  city: City;
}
