from django.urls import path
from .views import ShortenURLView, RedirectView, URLHistoryView

urlpatterns = [
    path("api/shorten/", ShortenURLView.as_view(), name="shorten-url"),
    path("api/history/", URLHistoryView.as_view(), name="url-history"),
    path("<str:code>/", RedirectView.as_view(), name="redirect-url"),
]
