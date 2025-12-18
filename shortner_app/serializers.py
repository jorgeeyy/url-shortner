from rest_framework import serializers
from .models import ShortenedURL
from django.contrib.auth.models import  User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .services.client_ip import get_client_ip, claim_anonymous_urls


class ShortURLCreateSerializer(serializers.ModelSerializer):
    original_url = serializers.URLField(max_length=2048)

    class Meta:
        model = ShortenedURL
        fields = ["original_url"]

    # def create(self, validated_data):
    #     request = self.context["request"]
    #
    #     if request.user.is_authenticated:
    #         validated_data["user"] = request.user
    #     else:
    #         validated_data["ip_address"] = get_client_ip(request)
    #
    #     return super().create(validated_data)


class ShortURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortenedURL
        fields = [
            "id",
            "original_url",
            "short_code",
            "created_at",
            "total_clicks",
            "is_active",
            # "user",
            "ip_address",
        ]
        read_only_fields = ["user", "total_clicks", "created_at"]

    def get_user(self, obj):
        if obj.user:
            return {
                "id": obj.user.id,
                "username": obj.user.username,
            }
        return None


class RegisterSerializer(serializers.ModelSerializer):
    password= serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    # first_name = serializers.CharField(required=True)
    # last_name = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        request = self.context["request"]
        ip = get_client_ip(request)
        claim_anonymous_urls(self.user, ip)

        return data
