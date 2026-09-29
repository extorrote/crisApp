import os
from PIL import Image as PilImage, ImageOps


def optimize_image(field, max_width=1200, quality=80):
    """
    Convierte cualquier ImageField a WebP optimizado.
    Mantiene transparencia (RGBA) si la imagen la tiene.
    Retorna el nuevo nombre relativo .webp, o None si no hubo conversión.
    """
    if not field or not field.name:
        return None

    path = field.path

    if path.endswith('.webp'):
        return None

    if not os.path.isfile(path):
        return None

    try:
        img = PilImage.open(path)
        img = ImageOps.exif_transpose(img)

        # Mantener transparencia si la imagen la tiene (PNG sin fondo, logos, etc.)
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            img = img.convert('RGBA')
        else:
            img = img.convert('RGB')

        if img.width > max_width:
            ratio      = max_width / img.width
            new_height = int(img.height * ratio)
            img        = img.resize((max_width, new_height), PilImage.LANCZOS)

        webp_path = os.path.splitext(path)[0] + '.webp'
        img.save(webp_path, 'WEBP', quality=quality, optimize=True)

        if os.path.exists(path):
            os.remove(path)

        return os.path.splitext(field.name)[0] + '.webp'

    except Exception as e:
        print(f'[optimize_image] Error procesando {field.name}: {e}')
        return None