# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from customuser.models import CustomUser
from establishment.models import EstablishmentModel
from django.contrib.auth import authenticate
from dataclasses import asdict
import time

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
            })
        return Response(
            {'detail': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user: CustomUser = request.user
        return Response(user.to_entity().model_dump())

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # No SimpleJWT, o logout é feito no cliente apenas removendo o token
        return Response({"detail": "Successfully logged out."})
    
class VerifyTokenView(APIView):
    def post(self, request):
        try:
            # Tenta autenticar (o SimpleJWT já verifica o token automaticamente)
            auth = JWTAuthentication()
            auth.get_validated_token(request.headers.get('Authorization').split(' ')[1])
            return Response({"valid": True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"valid": False, "error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)