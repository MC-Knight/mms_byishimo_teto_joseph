from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers, exceptions
from users.models import User
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "telephone",
            "user_type",
            "password",
            "password_confirm",
        ]
        read_only_fields = [
            "id",
        ]

    def validate(self, data):
        password = data.get("password")
        password_confirm = data.get("password_confirm")
        if password != password_confirm:
            raise exceptions.ParseError("Password don't match.")
        return data

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        validated_data.pop("password_confirm", None)
        instance = self.Meta.model(**validated_data)
        instance.set_password(password)
        instance.save()
        return instance

    def to_internal_value(self, data):
        telephone = data.get("telephone", None)
        if telephone:
            try:
                User.objects.get(telephone=telephone)
                raise exceptions.ParseError("Phone number already exists.")
            except User.DoesNotExist:
                pass

        return super().to_internal_value(data)


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "telephone",
            "first_name",
            "last_name",
            "user_type",
        ]
        read_only_fields = ["id", "user_type"]


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get("telephone")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"), username=username, password=password
        )

        if user is not None:
            refresh = self.get_token(user)

            data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            return data
        elif type(user) == list:
            raise exceptions.ParseError({"status": user[2], "message": user[2]})
        else:
            raise exceptions.ParseError("Wrong telephone number or password")

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["role"] = user.user_type
        token["telephone"] = user.telephone

        return token
