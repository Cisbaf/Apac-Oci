from rest_framework.views import APIView
from rest_framework.response import Response
from .models import EstablishmentModel
from .serializers import EstablishmentSerializer
from customuser.models import CustomUser

class EstablishmentApiView(APIView):
    def get(self, request):
        user: CustomUser = request.user
        establishments = (
            EstablishmentModel.objects
            .filter(city=user.city, is_active=True)
            .exclude(restricted_user=user)
        )
        serializer = EstablishmentSerializer(establishments, many=True)
        return Response(serializer.data)