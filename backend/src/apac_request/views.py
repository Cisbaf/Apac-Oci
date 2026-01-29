from pydantic import ValidationError
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from apac_core.application.use_cases.apac_request_cases.create_apac_request_case import (
    CreateApacRequestDTO, CreateApacRequestUseCase
)
from apac_core.domain.messages.apac_request_messages import SUCCESSFULLY_REGISTERED
from apac_request.controller import ApacRequestController
from apac_batch.controller import ApacBatchController
from apac_data.controller import ApacDataController
from establishment.controller import EstablishmentController
from customuser.controller import UserController
from procedure.controller import ProcedureController, CidController
from procedure_record.controller import ProcedureRecordController
from apac_core.application.use_cases.apac_request_cases.authorize_apac_request_case import ApprovedApacRequestUseCase, RejectApacRequestUseCase, ApprovedApacRequestDTO, RejectApacRequestDTO
from .models import ApacRequestModel
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Q
from django.shortcuts import render
from collections import defaultdict
from apac_core.application.ultils.formart_errors import format_validation_errors


class ApacRequestListCreate(APIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        status = request.query_params.get('status')
        id = request.query_params.get('id')
        if id:
            try: 
                model_apac = ApacRequestModel.objects.get(pk=id)
                if model_apac.requester != request.user:
                    return Response("Não autorizado!", status=400)
                entity = model_apac.to_entity()
                return Response(data=[entity.model_dump()])
            except:
                return Response("Não encontrado!", status=400)

        models_apac = ApacRequestModel.objects.filter(
            establishment__city=request.user.city,
            status=status,
            apac_data__procedure_date__range=(start_date, end_date)
        )
        lenght = len(models_apac)
        if lenght < 1:
            return Response({
                "message": "Nenhum registro encontrado!",
            }, status=400)
        
        entities_apac = [apac.to_entity(exclude_cid_procedures=True, exclude_sub_procedures_for_main=True) for apac in models_apac]
        return Response({
            "message": f"{lenght} solicitações encontradas!",
            "data":  [entity.model_dump() for entity in entities_apac]
        })

    @transaction.atomic
    def post(self, request):
        try:
            apac_request = CreateApacRequestUseCase(
                repo_apac_request=ApacRequestController(),
                repo_user=UserController(),
                repo_establishment=EstablishmentController(),
                repo_apac_data=ApacDataController(),
                repo_cid=CidController(),
                repo_procedure=ProcedureController(),
                repo_procedure_record=ProcedureRecordController(),
            ).execute(CreateApacRequestDTO(**request.data))

            return Response({
                "message": SUCCESSFULLY_REGISTERED,
                "apac_request_id": apac_request.id
            }, status=status.HTTP_200_OK)
        
        except ValidationError as e:
            formatted = format_validation_errors(e.errors())
            return Response({"message": formatted}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ApacRequestApprovedAPIView(APIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        try:
            ApprovedApacRequestUseCase(
                repo_apac_request=ApacRequestController(),
                repo_user=UserController(),
                repo_apac_batch=ApacBatchController()
            ).execute(ApprovedApacRequestDTO(**request.data))
            return Response({"message": "Solicitação aprovada!"})
        except Exception as e:
            return Response({"message": str(e)}, status=403)
        

class ApacRequestRejectAPIView(APIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        try:
            RejectApacRequestUseCase(
                repo_apac_request=ApacRequestController(),
                repo_user=UserController()
            ).execute(RejectApacRequestDTO(**request.data))
            return Response({"message": "Solicitação rejeitada!"})
        except Exception as e:
            return Response({"message": str(e)}, status=403)

@staff_member_required
def apac_dashboard(request):
    base_query = ApacRequestModel.objects.all()
    if not request.user.is_superuser:
        base_query = base_query.filter(establishment__city=request.user.city)

    grouped_data = (
        base_query
        .values("establishment__city__name", "establishment__name", "status")
        .annotate(total=Count("id"))
        .order_by("establishment__city__name", "establishment__name", "status")
    )

    # Estruturar: {estab_label: {status: count}}
    data_map = defaultdict(lambda: defaultdict(int))
    estab_labels = []

    for row in grouped_data:
        city = row["establishment__city__name"]
        estab = row["establishment__name"]
        status = row["status"] or "pending"
        count = row["total"]
        label = f"{estab} ({city})"
        data_map[label][status] = count
        if label not in estab_labels:
            estab_labels.append(label)

    statuses = ["rejected", "pending", "approved"]  # ordem invertida
    status_labels = {
        "approved": "Aprovadas",
        "pending": "Pendentes",
        "rejected": "Rejeitadas"
    }
    status_colors = {
        "approved": "#4CAF50",   # verde
        "pending": "#FFC107",    # amarelo
        "rejected": "#F44336"    # vermelho
    }
    datasets = []
    for status in statuses:
        data = [data_map[label].get(status, 0) for label in estab_labels]
        datasets.append({
            "label": status_labels[status],
            "data": data,
            "backgroundColor": status_colors[status],
            "borderWidth": 1,
        })

    context = {
        "labels": estab_labels,
        "datasets": datasets,
    }
    return render(request, "apac_dashboard.html", context)