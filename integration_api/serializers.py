from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
# from team.models import Team

User = get_user_model()

# TODO : Incrementar o id do grupo de usuários

DEFAULT_USER_GROUP_ID = 1

class ExternalAdminUserSerializer(serializers.Serializer):
    
    username = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Este nome de usuário já está em uso."
            )
        ]
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Este e-mail já está em uso."
            )
        ]
    )
    password = serializers.CharField(write_only=True)
    stripe_subscription_id = serializers.CharField(write_only=True)

    def create(self, validated_data):
        # 1) cria user staff
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        user.is_staff = True
        user.save()


        try:
            default_group = Group.objects.get(pk=DEFAULT_USER_GROUP_ID)
            user.groups.add(default_group)
        except Group.DoesNotExist:
            raise serializers.ValidationError(
                "Grupo padrão (id=1) não existe. Crie-o antes de usar a API."
            )
        
        profile = user.profile
        stripe_subscription_id = validated_data.get("stripe_subscription_id")
        if stripe_subscription_id is not None:
            profile.stripe_subscription_id = stripe_subscription_id
        
        profile.save()

        return user
