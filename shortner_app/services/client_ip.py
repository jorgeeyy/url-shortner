from shortner_app.models import ShortenedURL
from django.utils.timezone import now
from datetime import timedelta


ANON_LIMIT = 5
ANON_WINDOW_HOURS = 24


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip

def can_create_anonymous_url(ip):
    today = now() - timedelta(days=1)
    return ShortenedURL.objects.filter(
        ip_address=ip,
        created_at__gte=today
    ).count() < 5


def can_create_anonymous_url(ip_address: str) -> bool:
    since = now() - timedelta(hours=ANON_WINDOW_HOURS)

    count = ShortenedURL.objects.filter(
        ip_address=ip_address,
        created_at__gte=since
    ).count()

    return count < ANON_LIMIT

def claim_anonymous_urls(user, ip_address):
    ShortenedURL.objects.filter(
        user__isnull=True,
        ip_address=ip_address
    ).update(
        user=user,
        ip_address=None
    )
