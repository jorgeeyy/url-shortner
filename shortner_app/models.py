from django.db import models


# Create your models here.
class ShortenedURL(models.Model):
    original_url = models.URLField(max_length=2048)
    short_code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    qr_code_image = models.ImageField(upload_to="qr_codes/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    total_clicks = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"
