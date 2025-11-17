import qrcode
from django.core.files.base import ContentFile
from io import BytesIO


def generate_qr_code(data: str):
    qr = qrcode.make(data)
    bufer = BytesIO()
    qr.save(bufer, format="PNG")

    return ContentFile(bufer.getvalue(), name="qr_code.png")
