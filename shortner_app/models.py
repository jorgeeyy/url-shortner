from django.db import models
from django.conf import settings


# Create your models here.
class ShortenedURL(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
    null=True, blank=True,
    on_delete=models.CASCADE, related_name="user")

    original_url = models.URLField(max_length=2048)
    short_code = models.CharField(max_length=10, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    qr_code_image = models.ImageField(upload_to="qr_codes/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    total_clicks = models.PositiveIntegerField(default=0)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"