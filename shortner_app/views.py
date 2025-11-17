# from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ShortURLCreateSerializer, ShortURLSerializer
from django.shortcuts import get_object_or_404, redirect
from .services.url_service import create_shortened_url
from .models import ShortenedURL

# from django.utils import timezone


class ShortenURLView(APIView):
    serialzer_class = ShortURLCreateSerializer

    def post(self, request):
        serializer = ShortURLCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        url_object = create_shortened_url(serializer.validated_data["original_url"])
        return Response(
            ShortURLSerializer(url_object).data, status=status.HTTP_201_CREATED
        )


class RedirectView(APIView):
    def get(self, request, code):
        url_object = get_object_or_404(ShortenedURL, short_code=code, is_active=True)
        url_object.total_clicks += 1
        url_object.save()
        return redirect(url_object.original_url)


class URLHistoryView(APIView):
    def get(self, request):
        urls = ShortenedURL.objects.all().order_by("-created_at")
        serializer = ShortURLSerializer(urls, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
