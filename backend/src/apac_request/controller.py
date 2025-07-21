from .models import ApacRequestModel
from establishment.models import EstablishmentModel
from customuser.models import CustomUser
from apac_data.models import ApacDataModel
from apac_core.domain.repositories.apac_request_repository import ApacRequestRepository
from apac_core.domain.exceptions import NotFoundException


class ApacRequestController(ApacRequestRepository):

    def get_by_id(self, id):
        apac_request = ApacRequestModel.objects.get(pk=id)
        if apac_request:
            return apac_request.to_entity()
        raise NotFoundException()
    
    def save(self, apac_request):
        if apac_request.id:
            apac_request_model = ApacRequestModel.objects.get(pk=apac_request.id)
            apac_request_model.status = apac_request.status
            apac_request_model.authorizer = CustomUser.objects.get(pk=apac_request.authorizer.id)
            apac_request_model.justification = apac_request.justification
            apac_request_model.review_date = apac_request.review_date
            apac_request_model.save()
            return apac_request_model.to_entity()

        apac_request_model = ApacRequestModel.objects.create(
            establishment=EstablishmentModel.objects.get(pk=apac_request.establishment.id),
            requester=CustomUser.objects.get(pk=apac_request.requester.id),
        )
        apac_data = ApacDataModel.objects.get(pk=apac_request.apac_data.id)
        if apac_data:
            apac_data.apac_request = apac_request_model
            apac_data.save()
        return apac_request_model.to_entity()