from django.test import TestCase
from apac_core.application.use_cases.create_apac_data_case import CreateApacDataDTO

PATIENT_DATA = {
    "patient_name": "João da Silva",
    "patient_record_number": "",
    "patient_cns": "706000343458946",
    "patient_cpf": "187.149.337-48",
    "patient_birth_date": "1999-03-12",
    "patient_race_color": "parda",
    "patient_gender": "Masculino",
    "patient_mother_name": "Maria Aparecida da Silva",
    "patient_address_street_type": "Avenida",
    "patient_address_street_name": "Abilio Augusto Tavora",
    "patient_address_number": "2789",
    "patient_address_complement": "Apartamento 201", # opcional
    "patient_address_postal_code": "26265-090",
    "patient_address_neighborhood": "Jardim Alvorada",
    "patient_address_city": "Nova Iguaçu",
    "patient_address_state": "RJ",
    "supervising_physician_name": "Fernando Rodrigues",
    "supervising_physician_cns": "706000343458946",
    "supervising_physician_cbo": "20154786",
    "authorizing_physician_name": "Fernando Rodrigues",
    "authorizing_physician_cns": "706000343458946",
    "authorizing_physician_cbo": "20154786",
    "procedure_date": "2025-07-30",
    "discharge_date": "2025-07-29",
    "cid_id": 1,
    "main_procedure_id": 1,
    "sub_procedures": []
}



class BaseApacTest(TestCase):

    def test_create_entity(self):
        CreateApacDataDTO(**PATIENT_DATA)