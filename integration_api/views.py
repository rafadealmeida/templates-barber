from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, authentication
from .authentication import APIKeyAuthentication
from .serializers import ExternalAdminUserSerializer

class ExternalAdminUserCreateView(APIView):
    authentication_classes = [APIKeyAuthentication]
    permission_classes = [permissions.AllowAny]


    def post(self, request):
        serializer = ExternalAdminUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        profile = user.profile
        return Response({
            "username": user.username,
            "email": user.email,
            "stripe_subscription_id": profile.stripe_subscription_id,
        }, status=status.HTTP_201_CREATED)

