from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import ShortenURLView, RedirectView, URLHistoryView, SignupView, CustomTokenObtainPairView

urlpatterns = [
    path("api/shorten/", ShortenURLView.as_view(), name="shorten-url"),
    path("api/history/", URLHistoryView.as_view(), name="url-history"),
    path("<str:code>/", RedirectView.as_view(), name="redirect-url"),
    path("api/auth/signup/", SignupView.as_view()),
    path("api/auth/login/", CustomTokenObtainPairView.as_view()),
    # path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

]
