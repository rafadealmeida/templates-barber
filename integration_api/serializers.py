from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
# from team.models import Team

User = get_user_model()

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
    # team_id = serializers.IntegerField()

    # def validate_team_id(self, value):
    #     if not Team.objects.filter(pk=value).exists():
    #         raise serializers.ValidationError("Time não encontrado.")
    #     return value

    def create(self, validated_data):
        # 1) cria user staff
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        user.is_staff = True
        user.save()


        # 2) vincula ao grupo alvo
        # group, _ = Group.objects.get_or_create(name="NomeDoGrupoAlvo")
        # user.groups.add(group)

        # 3) adiciona ao time
        # Team.objects.get(pk=validated_data["team_id"]).members.add(user)
        
        profile = user.profile
        stripe_subscription_id = validated_data.get("stripe_subscription_id")
        if stripe_subscription_id is not None:
            profile.stripe_subscription_id = stripe_subscription_id
        
        profile.save()

        return user
