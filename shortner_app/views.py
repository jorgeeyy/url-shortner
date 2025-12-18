# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import ShortURLCreateSerializer, ShortURLSerializer, RegisterSerializer, \
    CustomTokenObtainPairSerializer
from django.shortcuts import get_object_or_404, redirect
from django.db.models import F
from .services.client_ip import get_client_ip, can_create_anonymous_url, claim_anonymous_urls
from .services.url_service import create_shortened_url
from .models import ShortenedURL
from rest_framework.permissions import AllowAny, IsAuthenticated


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        ip = get_client_ip(request)
        claim_anonymous_urls(user, ip)

        return Response(
            {"message": "User registered successfully"},
            status=status.HTTP_201_CREATED
        )

    # def post(self, request):
    #     serializer = RegisterSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(
    #             {"message": "User registered successfully"},
    #             status=status.HTTP_201_CREATED
    #         )
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShortenURLView(APIView):
    serialzer_class = ShortURLCreateSerializer
    permission_classes = [AllowAny]
    queryset = ShortenedURL.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return ShortenedURL.objects.filter(user=user)
        return ShortenedURL.objects.none()

    def post(self, request):
        serializer = ShortURLCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.user.is_authenticated:
            url_object = create_shortened_url(serializer.validated_data["original_url"],
                                              user=request.user, )
        else:
            ip = get_client_ip(request)

            if not can_create_anonymous_url(ip):
                return Response(
                    {"detail": "Anonymous limit reached. Please sign up or try again"},
                    status=status.HTTP_429_TOO_MANY_REQUESTS
                )
            url_object = create_shortened_url(
                serializer.validated_data["original_url"],
                ip_address=ip
            )
        return Response(
            ShortURLSerializer(url_object).data,
            status=status.HTTP_201_CREATED
        )


class RedirectView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, code):
        url_object = get_object_or_404(ShortenedURL, short_code=code, is_active=True)
        url_object.total_clicks = F("total_clicks") + 1
        url_object.save(update_fields=["total_clicks"])
        return redirect(url_object.original_url)


class URLHistoryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            urls = ShortenedURL.objects.filter(user=request.user)
        else:
            ip = get_client_ip(request)
            urls = ShortenedURL.objects.filter(ip_address=ip)

        serializer = ShortURLSerializer(urls.order_by("-created_at"), many=True)
        return Response(serializer.data)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



# class URLHistoryView(APIView):
#     permission_classes = [AllowAny]
#     def get(self, request):
#         urls = ShortenedURL.objects.all().order_by("-created_at")
#         serializer = ShortURLSerializer(urls, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
