import io

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont


def make_watermarked_thumbnail(file):
    image = Image.open(file).convert('RGB')
    image.thumbnail((300, 300))

    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default(24)
    left, top, right, bottom = draw.textbbox((0, 0), 'Shop', font)
    pos = (image.width - right - 8, image.height - bottom - 8)
    draw.text(pos, 'Shop', 'white', font, stroke_width=1, stroke_fill='black')

    buffer = io.BytesIO()
    image.save(buffer, 'JPEG')
    return ContentFile(buffer.getvalue(), file.name)
