import re
from typing import List
from apac_core.domain.exceptions import NotFoundException
from apac_core.domain.repositories.apac_request_repository import ApacRequestRepository
from apac_core.domain.entities.apac_request import ApacRequest


class ApacRequestFakeRepository(ApacRequestRepository):

    def __init__(self):
        super().__init__()
        self.increment_id = 1
        self.apac_requests: List[ApacRequest] = []
    
    def save(self, apac_request):
        if not apac_request.id:
            apac_request.id = self.increment_id
            self.increment_id += 1
            self.apac_requests.append(apac_request)
        else:
            for i, _apac_request in enumerate(self.apac_requests):
                if _apac_request.id == apac_request.id:
                    self.apac_requests[i] = apac_request
                    break
        return apac_request

    def get_by_id(self, id):
        for apac_request in self.apac_requests:
            if apac_request.id == id:
                return apac_request
        raise NotFoundException()

    def check_duplicates(self, establishment_id, patient_cpf, main_procedure, request_date):
        cpf_digits = re.sub(r"\D", "", patient_cpf)
        return any(
            apac_request.establishment.id == establishment_id
            and apac_request.apac_data.patient_data.cpf.value == cpf_digits
            and apac_request.apac_data.main_procedure.id == main_procedure
            and apac_request.request_date.year == request_date.year
            and apac_request.request_date.month == request_date.month
            for apac_request in self.apac_requests
        )