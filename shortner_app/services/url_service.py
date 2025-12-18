from django.conf import settings
from shortner_app.models import ShortenedURL

# from .base62 import encode_base62
from .qr_generation import generate_qr_code
import random
import string


def generate_random_string(length: int = 6) -> str:
    chars = string.ascii_letters + string.digits
    while True:
        random_str = "".join(random.choices(chars, k=length))
        if not ShortenedURL.objects.filter(short_code=random_str).exists():
            return random_str


def create_shortened_url(
    original_url: str,
    *,
    user=None,
    ip_address=None
) -> ShortenedURL:
    url_object = ShortenedURL.objects.create(
        original_url=original_url,
        user=user,
        ip_address=ip_address,
    )

    code = generate_random_string(6)
    while ShortenedURL.objects.filter(short_code=code).exists():
        code = generate_random_string(6)

    url_object.short_code = code

    short_link = f"{settings.SITE_URL}/{code}"
    qr_image = generate_qr_code(short_link)
    url_object.qr_code_image.save(f"{code}_qr.png", qr_image)

    url_object.save()
    return url_object
