from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError
from apps.user.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email"]
