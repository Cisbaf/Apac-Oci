from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ProcedureModel
from .serializers import ProcedureSerializer


class ProcedureApiView(APIView):
    def get(self, request):
        procedures = ProcedureModel.objects.filter(is_active=True, parent=None)
        serializer = ProcedureSerializer(procedures, many=True)
        return Response(serializer.data)
