from rest_framework.views import APIView
from apac_batch.models import ApacBatchModel
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from apac_core.application.use_cases.apac_export_case import ApacExportCase, ApacExportDto
from apac_batch.controller import ApacBatchController
from establishment.controller import EstablishmentController
from apac_core.application.ultils.formart_errors import format_validation_errors
from pydantic import ValidationError
from rest_framework import status

class ApacBatchsAvailable(APIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        competence_month = request.query_params.get('competence_month')
        competence_year = request.query_params.get('competence_year')
        establishment_id = request.query_params.get("establishment_id")

        if not competence_month or not competence_year or not establishment_id:
            return Response(data={}, status=400)

        batchs = ApacBatchModel.objects.filter(
            apac_request__isnull=False,  # só pega os que possuem apac_request
            apac_request__request_date__month=competence_month,
            apac_request__request_date__year=competence_year,
            apac_request__establishment__id=establishment_id,
            apac_request__status="approved",
            city=request.user.city
        )
        
        entities = [batch.to_entity(exclude_cid_procedures=True, exclude_sub_procedures_for_main=True) for batch in list(batchs)]

        return Response([entity.model_dump() for entity in entities])
    

class ExportApacBatch(APIView):

    def post(self, request):
        try:
            content_extract = ApacExportCase(
                repo_apac_batch=ApacBatchController(),
                repo_establishment=EstablishmentController()
            ).execute(ApacExportDto(**request.data))
            return Response({"content": content_extract})
        except ValidationError as e:
            formatted = format_validation_errors(e.errors())
            return Response({"message": formatted}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)