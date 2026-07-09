from datetime import date, datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ProcedureModel
from .serializers import ProcedureSerializer


class ProcedureApiView(APIView):
    def get(self, request):
        procedures = ProcedureModel.objects.filter(parents=None, is_active=True)
        serializer = ProcedureSerializer(procedures, many=True)
        return Response(serializer.data)


# Regras de alerta de idade por código de procedimento (cod_sig_tap).
# Placeholder: as faixas etárias reais (ex. integração SIGTAP/DATASUS) ainda
# não foram definidas, então este dicionário existe apenas para validar o
# fluxo de aviso ponta a ponta e fica vazio por padrão (nenhum alerta disparado).
PROCEDURE_AGE_ALERT_RULES = {}


def _calculate_age(birth_date: date, reference_date: date) -> int:
    age = reference_date.year - birth_date.year
    if (reference_date.month, reference_date.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age


class ProcedureAgeAlertApiView(APIView):
    """Checa se a idade do paciente está fora da faixa esperada para o procedimento.

    Retorna sempre 200 com alert=False quando não há regra cadastrada para o
    procedimento, já que a ausência de dados não deve travar o solicitante.
    """

    def post(self, request):
        procedure_id = request.data.get("procedure_id")
        birth_date_raw = request.data.get("birth_date")

        if not procedure_id or not birth_date_raw:
            return Response(
                {"detail": "procedure_id e birth_date são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            birth_date = datetime.strptime(birth_date_raw, "%Y-%m-%d").date()
        except (TypeError, ValueError):
            return Response(
                {"detail": "birth_date deve estar no formato YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        procedure = ProcedureModel.objects.filter(pk=procedure_id).first()
        if not procedure:
            return Response(
                {"detail": "Procedimento não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        age = _calculate_age(birth_date, date.today())
        rule = PROCEDURE_AGE_ALERT_RULES.get(procedure.code)

        if not rule:
            return Response({"alert": False, "age": age})

        min_age, max_age = rule.get("min_age"), rule.get("max_age")
        out_of_range = (min_age is not None and age < min_age) or (
            max_age is not None and age > max_age
        )

        if not out_of_range:
            return Response({"alert": False, "age": age})

        return Response({
            "alert": True,
            "age": age,
            "message": rule.get(
                "message",
                f"O paciente tem {age} anos, fora da faixa etária esperada para este procedimento.",
            ),
        })
