from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse,
)

from .serializers import ExternalAdminUserSerializer
from .authentication import APIKeyAuthentication
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

@extend_schema(
    tags=["External"],
    summary="Cria um usuário admin externo",
    description="Cria um usuário staff e preenche o stripe_subscription_id no profile.",
    request=ExternalAdminUserSerializer,
    responses={201: {"type": "object", "properties": {
        "username": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "stripe_subscription_id": {"type": "string"}
    }}},
    # Você pode manter a segurança global, mas aqui vai um exemplo explícito:
    auth=[{"ApiKeyAuth": []}],
    parameters=[
        OpenApiParameter(
            name="X-API-KEY",
            type=str,
            location=OpenApiParameter.HEADER,
            required=True,
            description="Chave da integração."
        )
    ],
    examples=[
        OpenApiExample(
            "Exemplo de criação",
            value={
                "username": "novo_admin1",
                "email": "admin1@exemplo.com",
                "password": "SenhaForte!2025",
                "stripe_subscription_id": "teste"
            },
        )
    ],
)
class ExternalAdminUserCreateView(APIView):
    permission_classes = [permissions.AllowAny]  # sua auth por API key já barra
    # authentication_classes = [APIKeyAuthentication]  # se não estiver global

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
