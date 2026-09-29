from django.shortcuts import render,redirect,HttpResponse
from .models import NewsletterSubscription ,ContactMessage# Assuming you have a model defined for subscriptions
# Create your views here.



from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.views.decorators.http import require_http_methods
import logging

from .models import NewsletterSubscription, ContactMessage, Subscriber,Proyecto
from .forms import ContactForm, SubscriberForm

logger = logging.getLogger(__name__)


def send_email(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name    = form.cleaned_data['name']
            email   = form.cleaned_data['email']
            phone   = form.cleaned_data['phone']
            message = form.cleaned_data['message']

            ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                message=message
            )

            try:
                send_mail(
                    subject=f'Nuevo mensaje de contacto de {name}',
                    message=f'Nombre: {name}\nEmail: {email}\nTeléfono: {phone}\n\nMensaje:\n{message}\n\n---\nResponder a: {email}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['proyectodigitalmexico@gmail.com'],
                    fail_silently=False,
                )
                messages.success(request, '¡Gracias por tu mensaje! Te responderemos pronto.')
                return redirect('enviar_email')
            except Exception as e:
                logger.error(f"Error enviando email: {e}")
                messages.error(request, 'Hubo un error. Por favor intenta nuevamente.')
        else:
            if 'captcha' in form.errors:
                messages.error(request, 'Verificación de seguridad fallida. Intenta nuevamente.')
            else:
                messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = ContactForm()

    subscriber_form = SubscriberForm()
    return render(request, 'inicio.html', {
        'form': form,
        'subscriber_form': subscriber_form,
    })


@require_http_methods(["GET", "POST"])
def suscribirse(request):
    if request.method == 'POST':
        if request.POST.get('website', ''):
            messages.success(request, 'Successfully subscribed!')
            return redirect('inicio')

        email  = request.POST.get('email', '').strip()
        nombre = request.POST.get('nombre', '').strip()

        if not email:
            messages.error(request, 'Please fill in your email.')
            return redirect('inicio')

        if NewsletterSubscription.objects.filter(email=email).exists():
            messages.warning(request, 'This email is already subscribed!')
        else:
            NewsletterSubscription.objects.create(email=email)
            messages.success(request, 'Successfully subscribed!')

        return redirect('inicio')

    contact_form    = ContactForm()
    subscriber_form = SubscriberForm()
    return render(request, 'inicio.html', {
        'form': contact_form,
        'subscriber_form': subscriber_form,
    })


def home(request):
    contact_form    = ContactForm()
    subscriber_form = SubscriberForm()
    proyectos=Proyecto.objects.filter(activo=True)
    return render(request, 'inicio.html', {
        'form': contact_form,
        'subscriber_form': subscriber_form,
        'proyectos':proyectos,
    })


def politica_privacidad(request):
    return render(request ,'politica_privacidad.html')


def terminos_condiciones(request):
    return render(request ,'terminos_condiciones.html')

def about_us(request):
    return render(request,'about_us.html')





# views.py




from .models import NewsletterSubscription

def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if email:
            subscription = NewsletterSubscription(email=email)
            subscription.save()
            messages.success(request, "Thank you for subscribing to our newsletter!")
            return redirect('inicio')  # Change this to an existing view name

        messages.error(request, "Invalid email address.")

    return redirect('inicio')  # Change this accordingly



def carta_silvia(request):
    return render(request , 'carta_recomendacion.html')





import qrcode
import base64
from io import BytesIO
from django.shortcuts import render
import random
from PIL import Image, ImageDraw, ImageFont
import os

def generar_qr(request):
    qr_personalizado = None
    qr_variantes = []

    # Valores por defecto
    numero = ""
    mensaje = ""
    url = ""
    tipo_qr = "whatsapp"
    color1 = "#000000"
    color2 = "#000000"
    color3 = "#000000"
    fondo = "#ffffff"
    text_color = "#000000"
    icono_file = None
    wifi_ssid = ""
    wifi_password = ""
    wifi_tipo = "WPA"

    if request.method == "POST":
        numero = request.POST.get("numero", "")
        mensaje = request.POST.get("mensaje", "")
        url = request.POST.get("url", "")
        tipo_qr = request.POST.get("tipo_qr", "whatsapp")
        color1 = request.POST.get("color1", "#000000")
        color2 = request.POST.get("color2", "#000000")
        color3 = request.POST.get("color3", "#000000")
        fondo = request.POST.get("fondo", "#ffffff")
        text_color = request.POST.get("text_color", "#000000")
        accion = request.POST.get("accion")
        icono_file = request.FILES.get("icono")
        wifi_ssid = request.POST.get("wifi_ssid", "")
        wifi_password = request.POST.get("wifi_password", "")
        wifi_tipo = request.POST.get("wifi_tipo", "WPA")

        # -------------------------------------------------------
        # WHATSAPP: genera enlace directo a chat de WhatsApp
        # -------------------------------------------------------
        if tipo_qr == "whatsapp" and numero:
            enlace = f"https://wa.me/{numero}"

        # -------------------------------------------------------
        # PÁGINA WEB: genera enlace a cualquier URL
        # -------------------------------------------------------
        elif tipo_qr == "web" and url:
            enlace = url

        # -------------------------------------------------------
        # WIFI: genera string estándar que iOS/Android reconocen
        # para conectarse automáticamente a la red al escanear
        # Formato: WIFI:T:<seguridad>;S:<ssid>;P:<contraseña>;;
        # -------------------------------------------------------
        elif tipo_qr == "wifi" and wifi_ssid:
            enlace = f"WIFI:T:{wifi_tipo};S:{wifi_ssid};P:{wifi_password};;"

        else:
            enlace = ""

        # Función para agregar ícono central al QR
        def agregar_cuadro_con_icono(qr_img, icono=None, tamaño_icono=100):
            qr = qr_img.convert("RGBA")
            ancho, alto = qr.size
            x0 = (ancho - tamaño_icono) // 2
            y0 = (alto - tamaño_icono) // 2
            if icono:
                icono = icono.convert("RGBA")
                icono = icono.resize((tamaño_icono, tamaño_icono))
                qr.paste(icono, (x0, y0), icono)
            return qr

        # Función para generar QR con gradiente de 3 colores
        def generar_qr_img(colors, back):
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(enlace)
            qr.make(fit=True)

            def hex_to_rgba(hex_color):
                if not hex_color or not isinstance(hex_color, str):
                    hex_color = "#000000"
                hex_color = hex_color.strip()
                if not hex_color.startswith("#"):
                    hex_color = "#" + hex_color
                hex_clean = hex_color.lstrip("#")
                if len(hex_clean) != 6:
                    hex_clean = "000000"
                try:
                    return tuple(int(hex_clean[i:i+2], 16) for i in (0, 2, 4)) + (255,)
                except ValueError:
                    return (0, 0, 0, 255)

            back_color = hex_to_rgba(back)
            img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
            ancho, alto = img.size
            grad = Image.new("RGBA", img.size, back_color)

            c0 = hex_to_rgba(colors[0])
            c1 = hex_to_rgba(colors[1])
            c2 = hex_to_rgba(colors[2])

            for y in range(alto):
                ratio = y / alto
                if ratio < 0.5:
                    ratio2 = ratio * 2
                    c = tuple(int(c0[i]*(1-ratio2) + c1[i]*ratio2) for i in range(4))
                else:
                    ratio2 = (ratio - 0.5) * 2
                    c = tuple(int(c1[i]*(1-ratio2) + c2[i]*ratio2) for i in range(4))

                for x in range(ancho):
                    pixel = img.getpixel((x, y))
                    if pixel[0] < 128:
                        grad.putpixel((x, y), c)

            img = grad

            if icono_file:
                icono = Image.open(icono_file)
                img = agregar_cuadro_con_icono(img, icono)
            return img

        def img_to_base64(img):
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            return base64.b64encode(buffer.getvalue()).decode("utf-8")

        if accion == "generar" and enlace:
            img = generar_qr_img([color1, color2, color3], fondo)
            qr_personalizado = img_to_base64(img)

        elif accion == "otros" and enlace:
            qr_variantes_post = request.POST.getlist("qr_variantes_base64[]")
            qr_variantes = [{"qr": q} for q in qr_variantes_post]

            nuevos_qr = []
            for _ in range(4):
                fill_colors = ["#{:06x}".format(random.randint(0, 0xFFFFFF)) for _ in range(3)]
                back = "#{:06x}".format(random.randint(0, 0xFFFFFF))
                img = generar_qr_img(fill_colors, back)
                nuevos_qr.append({"qr": img_to_base64(img)})

            qr_variantes = nuevos_qr + qr_variantes

    return render(request, "generar_qr.html", {
        "qr_personalizado": qr_personalizado,
        "qr_variantes": qr_variantes,
        "numero": numero,
        "mensaje": mensaje,
        "url": url,
        "tipo_qr": tipo_qr,
        "color1": color1,
        "color2": color2,
        "color3": color3,
        "fondo": fondo,
        "text_color": text_color,
        "wifi_ssid": wifi_ssid,
        "wifi_password": wifi_password,
        "wifi_tipo": wifi_tipo,
    })

# ─────────────────────────────────────────────────────────────────────────────
#  VISTA UNIFICADA — Convertir imágenes entre cualquier formato
#  Agregar a crisapp/views.py
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
#  VISTAS — crisapp/views.py
# ─────────────────────────────────────────────────────────────────────────────

import io
import os
import base64
import zipfile
import tempfile
import subprocess
import shutil

from PIL import Image
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.views.decorators.csrf import ensure_csrf_cookie
from .forms import ContactForm


# ══════════════════════════════════════════════════════════════════════════════
#  CONVERTIR IMÁGENES
# ══════════════════════════════════════════════════════════════════════════════

FORMATOS = {
    'webp':  ('WEBP',  'image/webp',      {'quality': 85}),
    'jpg':   ('JPEG',  'image/jpeg',      {'quality': 90, 'optimize': True}),
    'jpeg':  ('JPEG',  'image/jpeg',      {'quality': 90, 'optimize': True}),
    'png':   ('PNG',   'image/png',       {'optimize': True}),
    'gif':   ('GIF',   'image/gif',       {}),
    'bmp':   ('BMP',   'image/bmp',       {}),
    'tiff':  ('TIFF',  'image/tiff',      {}),
    'ico':   ('ICO',   'image/x-icon',    {}),
    'pdf':   ('PDF',   'application/pdf', {}),
}

FORMATOS_SIN_ALPHA = {'jpg', 'jpeg', 'bmp', 'gif', 'ico', 'pdf'}


def _preparar_imagen(img: Image.Image, fmt_destino: str) -> Image.Image:
    if fmt_destino in FORMATOS_SIN_ALPHA:
        if img.mode in ('RGBA', 'LA', 'P'):
            fondo = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            mascara = img.split()[-1] if img.mode in ('RGBA', 'LA') else None
            fondo.paste(img, mask=mascara)
            return fondo
        return img.convert('RGB')
    return img


def _guardar_ico(img: Image.Image, buf: io.BytesIO):
    """
    Genera un ICO con recorte circular y fondo transparente.
    Usa PNG compression interna (Vista+ format) para máxima compatibilidad
    con Windows, browsers y visores de imagen.
    """
    import struct
    from PIL import ImageDraw

    # ── Recorte cuadrado central ──────────────────────────────────
    img  = img.convert('RGBA')
    w, h = img.size
    lado = min(w, h)
    left = (w - lado) // 2
    top  = (h - lado) // 2
    img  = img.crop((left, top, left + lado, top + lado))

    # ── Máscara circular ──────────────────────────────────────────
    mask = Image.new('L', (lado, lado), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, lado, lado), fill=255)

    # ── Fondo transparente — el browser muestra el color del tab/OS ──
    result = Image.new('RGBA', (lado, lado), (0, 0, 0, 0))
    result.paste(img, mask=mask)

    # ── Generar frames PNG para cada tamaño estándar ──────────────
    sizes = [256, 128, 64, 48, 32, 16]
    png_frames = []
    for s in sizes:
        frame_buf = io.BytesIO()
        result.resize((s, s), Image.LANCZOS).save(frame_buf, format='PNG', optimize=True)
        png_frames.append(frame_buf.getvalue())

    # ── Construir ICO manualmente con PNG compression ─────────────
    # Formato: header(6) + n*directory_entry(16) + frame_data
    n      = len(png_frames)
    header = struct.pack('<HHH', 0, 1, n)   # reserved, type=1 (ico), count

    offset = 6 + n * 16  # inicio de los datos de imagen
    entries = b''
    for i, frame_data in enumerate(png_frames):
        s      = sizes[i]
        w_byte = 0 if s == 256 else s        # 256px se guarda como 0 en ICO
        entries += struct.pack('<BBBBHHII',
            w_byte, w_byte,   # width, height
            0,                # color count (0 = truecolor)
            0,                # reserved
            1,                # planes
            32,               # bits per pixel
            len(frame_data),  # tamaño del frame
            offset,           # offset al frame
        )
        offset += len(frame_data)

    buf.write(header + entries)
    for frame_data in png_frames:
        buf.write(frame_data)
    buf.seek(0)  # reset so callers can read from the beginning


@ensure_csrf_cookie
def convertir_imagenes(request):
    ctx = {'form': ContactForm()}

    if request.method == 'POST':

        # ── Formulario de contacto ────────────────────────────────────────────
        if 'name' in request.POST:
            contact_form = ContactForm(request.POST)
            if contact_form.is_valid():
                name    = contact_form.cleaned_data['name']
                email   = contact_form.cleaned_data['email']
                phone   = contact_form.cleaned_data['phone']
                message = contact_form.cleaned_data['message']
                send_mail(
                    f'Contact Form Submission from {name}',
                    f'Message: {message}\nPhone: {phone}\nEmail: {email}',
                    'proyectodigitalmexico@gmail.com',
                    ['proyectodigitalmexico@gmail.com'],
                    fail_silently=False,
                )
                messages.success(request, 'Email Sent! (Mensaje Enviado)')
            return redirect('convertir_imagenes')

        # ── Conversión de imágenes ────────────────────────────────────────────
        archivos    = request.FILES.getlist('imagenes')
        fmt_destino = request.POST.get('formato_destino', 'webp').lower().strip('.')

        if not archivos:
            messages.error(request, 'No se recibieron imágenes.')
            return render(request, 'convertir_imagenes.html', ctx)

        if fmt_destino not in FORMATOS:
            messages.error(request, f'Formato "{fmt_destino}" no soportado.')
            return render(request, 'convertir_imagenes.html', ctx)

        pil_fmt, mime_type, extra_kwargs = FORMATOS[fmt_destino]

        # ── PDF ───────────────────────────────────────────────────────────────
        if fmt_destino == 'pdf':
            paginas = []
            for archivo in archivos:
                try:
                    img = Image.open(archivo)
                    img = _preparar_imagen(img, 'pdf')
                    paginas.append(img)
                except Exception:
                    continue
            if not paginas:
                messages.error(request, 'No se pudo procesar ninguna imagen.')
                return render(request, 'convertir_imagenes.html', ctx)
            buf = io.BytesIO()
            paginas[0].save(buf, format='PDF', save_all=True, append_images=paginas[1:])
            buf.seek(0)
            resp = HttpResponse(buf, content_type='application/pdf')
            resp['Content-Disposition'] = 'attachment; filename="imagenes.pdf"'
            return resp

        # ── 1 imagen → descarga directa ───────────────────────────────────────
        if len(archivos) == 1:
            archivo = archivos[0]
            try:
                img = Image.open(archivo)
                img = _preparar_imagen(img, fmt_destino)
                buf = io.BytesIO()
                if fmt_destino == 'ico':
                    _guardar_ico(img, buf)
                else:
                    img.save(buf, format=pil_fmt, **extra_kwargs)
                buf.seek(0)
                nombre_base = archivo.name.rsplit('.', 1)[0]
                resp = HttpResponse(buf, content_type=mime_type)
                resp['Content-Disposition'] = f'attachment; filename="{nombre_base}.{fmt_destino}"'
                return resp
            except Exception as e:
                messages.error(request, f'Error al procesar la imagen: {e}')
                return render(request, 'convertir_imagenes.html', ctx)

        # ── Múltiples imágenes → ZIP ──────────────────────────────────────────
        zip_buf = io.BytesIO()
        with zipfile.ZipFile(zip_buf, 'w', zipfile.ZIP_DEFLATED) as zf:
            for archivo in archivos:
                try:
                    img = Image.open(archivo)
                    img = _preparar_imagen(img, fmt_destino)
                    img_buf = io.BytesIO()
                    if fmt_destino == 'ico':
                        _guardar_ico(img, img_buf)
                    else:
                        img.save(img_buf, format=pil_fmt, **extra_kwargs)
                    img_buf.seek(0)
                    nombre_out = archivo.name.rsplit('.', 1)[0] + f'.{fmt_destino}'
                    zf.writestr(nombre_out, img_buf.read())
                except Exception:
                    continue
        zip_buf.seek(0)
        resp = HttpResponse(zip_buf, content_type='application/zip')
        resp['Content-Disposition'] = f'attachment; filename="imagenes_convertidas_{fmt_destino}.zip"'
        return resp

    return render(request, 'convertir_imagenes.html', ctx)


# ══════════════════════════════════════════════════════════════════════════════
#  VIDEO A GIF
# ══════════════════════════════════════════════════════════════════════════════

def convertir_video_gif(request):
    if request.method != 'POST':
        return redirect('convertir_imagenes')

    video_file = request.FILES.get('video')
    if not video_file:
        return HttpResponse('No se recibió ningún video.', status=400, content_type='text/plain')

    try:
        fps      = max(1, min(int(request.POST.get('gif_fps', 10)), 24))
        width    = int(request.POST.get('gif_width', 480)) or 0
        start    = float(request.POST.get('gif_start', 0))
        duration = float(request.POST.get('gif_duration', 5))
    except (ValueError, TypeError):
        fps, width, start, duration = 10, 480, 0, 5

    suffix = os.path.splitext(video_file.name)[1].lower() or '.mp4'
    if suffix not in ('.mp4', '.mov', '.avi', '.webm', '.mkv', '.flv'):
        suffix = '.mp4'

    tmp_in_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_in:
            for chunk in video_file.chunks():
                tmp_in.write(chunk)
            tmp_in_path = tmp_in.name

        from moviepy import VideoFileClip

        clip = VideoFileClip(tmp_in_path)

        vid_end = clip.duration
        t_start = max(0.0, min(start, vid_end - 0.1))
        t_end   = (t_start + duration) if duration > 0 else vid_end
        t_end   = min(t_end, vid_end)
        if t_end > t_start:
            clip = clip.subclipped(t_start, t_end)

        if width and width > 0 and width != clip.w:
            clip = clip.resized(width=width)

        clip_fps   = min(fps, clip.fps or fps)
        frame_step = 1.0 / clip_fps
        times = []
        t = 0.0
        while t < clip.duration:
            times.append(t)
            t += frame_step

        if len(times) > 300:
            step = len(times) / 300
            times = [times[int(i * step)] for i in range(300)]

        frames_pil = []
        for t in times:
            try:
                frame_arr = clip.get_frame(t)
                img = Image.fromarray(frame_arr, 'RGB')
                img_q = img.quantize(
                    colors=256,
                    method=Image.Quantize.FASTOCTREE,
                    dither=Image.Dither.FLOYDSTEINBERG,
                )
                frames_pil.append(img_q)
            except Exception:
                continue

        clip.close()

        if not frames_pil:
            return HttpResponse(
                'No se pudieron extraer frames del video.',
                status=500, content_type='text/plain'
            )

        frame_duration_ms = int(1000 / clip_fps)
        buf = io.BytesIO()
        frames_pil[0].save(
            buf,
            format='GIF',
            save_all=True,
            append_images=frames_pil[1:],
            optimize=True,
            loop=0,
            duration=frame_duration_ms,
            disposal=2,
        )
        buf.seek(0)

        nombre_base = os.path.splitext(video_file.name)[0]
        resp = HttpResponse(buf.read(), content_type='image/gif')
        resp['Content-Disposition'] = f'attachment; filename="{nombre_base}_hq.gif"'
        return resp

    except Exception as e:
        import traceback
        traceback.print_exc()
        return HttpResponse(
            f'Error al convertir el video: {str(e)}',
            status=500, content_type='text/plain'
        )

    finally:
        if tmp_in_path:
            try:
                os.unlink(tmp_in_path)
            except Exception:
                pass


# ══════════════════════════════════════════════════════════════════════════════
#  QUITAR FONDO
# ══════════════════════════════════════════════════════════════════════════════

def quitar_fondo(request):
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'Método no permitido'}, status=405)

    imagen_file = request.FILES.get('imagen')
    if not imagen_file:
        return JsonResponse({'ok': False, 'error': 'No se recibió ninguna imagen.'}, status=400)

    try:
        from rembg import remove

        img_bytes    = imagen_file.read()
        result_bytes = remove(img_bytes)
        b64          = base64.b64encode(result_bytes).decode('utf-8')
        nombre_base  = imagen_file.name.rsplit('.', 1)[0]

        return JsonResponse({'ok': True, 'png_b64': b64, 'filename': nombre_base})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'ok': False, 'error': str(e)}, status=500)


def aplicar_fondo(request):
    if request.method != 'POST':
        return HttpResponse('Método no permitido', status=405)

    try:
        png_b64      = request.POST.get('png_b64', '')
        bg_color     = request.POST.get('bg_color', 'transparent')
        bg_gradient  = request.POST.get('bg_gradient', '')
        bg_image_b64 = request.POST.get('bg_image_b64', '')
        filename     = request.POST.get('filename', 'resultado')

        if not png_b64:
            return HttpResponse('No se recibió imagen.', status=400, content_type='text/plain')

        fg = Image.open(io.BytesIO(base64.b64decode(png_b64))).convert('RGBA')

        if bg_color == 'transparent' and not bg_gradient and not bg_image_b64:
            buf = io.BytesIO()
            fg.save(buf, format='PNG', optimize=True)
            buf.seek(0)
            resp = HttpResponse(buf, content_type='image/png')
            resp['Content-Disposition'] = f'attachment; filename="{filename}_sin_fondo.png"'
            return resp

        bg_img = Image.new('RGBA', fg.size, (255, 255, 255, 255))

        if bg_image_b64:
            bg_data = base64.b64decode(bg_image_b64)
            bg_img  = Image.open(io.BytesIO(bg_data)).convert('RGBA').resize(fg.size, Image.LANCZOS)

        elif bg_gradient:
            GRADIENTS = {
                'gradient-purple': ((102, 126, 234), (118, 75,  162)),
                'gradient-pink':   ((240, 147, 251), (245, 87,  108)),
                'gradient-blue':   ((79,  172, 254), (0,   242, 254)),
                'gradient-green':  ((67,  233, 123), (56,  249, 215)),
                'gradient-sunset': ((250, 112, 154), (254, 225, 64)),
            }
            c1, c2 = GRADIENTS.get(bg_gradient, ((255, 255, 255), (200, 200, 200)))
            w, h   = fg.size
            bg_img = Image.new('RGBA', fg.size)
            from PIL import ImageDraw
            draw = ImageDraw.Draw(bg_img)
            for x in range(w):
                r2 = x / w
                draw.line(
                    [(x, 0), (x, h)],
                    fill=(
                        int(c1[0] * (1 - r2) + c2[0] * r2),
                        int(c1[1] * (1 - r2) + c2[1] * r2),
                        int(c1[2] * (1 - r2) + c2[2] * r2),
                        255,
                    )
                )

        elif bg_color not in ('transparent', 'gradient', 'image'):
            hex_c = bg_color.lstrip('#')
            try:
                rgb    = tuple(int(hex_c[i:i+2], 16) for i in (0, 2, 4))
                bg_img = Image.new('RGBA', fg.size, rgb + (255,))
            except Exception:
                bg_img = Image.new('RGBA', fg.size, (255, 255, 255, 255))

        composite = Image.alpha_composite(bg_img, fg)
        buf = io.BytesIO()
        composite.convert('RGB').save(buf, format='PNG', optimize=True)
        buf.seek(0)

        suffix = '_sin_fondo' if bg_color == 'transparent' else '_nuevo_fondo'
        resp = HttpResponse(buf, content_type='image/png')
        resp['Content-Disposition'] = f'attachment; filename="{filename}{suffix}.png"'
        return resp

    except Exception as e:
        import traceback
        traceback.print_exc()
        return HttpResponse(f'Error: {str(e)}', status=500, content_type='text/plain')


# ══════════════════════════════════════════════════════════════════════════════
#  CONVERTIR VIDEO PARA WEB — procesamiento ASÍNCRONO con threads
#
#  Flujo:
#  1. POST /convertir-video/        → guarda video, lanza thread, devuelve job_id (JSON)
#  2. GET  /video-estado/<job_id>/  → devuelve estado: pending/done/error (JSON)
#  3. GET  /video-descarga/<job_id>/→ descarga el archivo terminado
# ══════════════════════════════════════════════════════════════════════════════

# Diccionario global para guardar trabajos en memoria
# { job_id: { 'status': 'pending'|'done'|'error', 'file': path, 'name': str,
#             'mime': str, 'error': str, 'created': float } }








import logging

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Sum

from .models import Confirmacion
from .forms import ConfirmacionForm

logger = logging.getLogger(__name__)


def invitacion(request):
    if request.method == 'POST':
        form = ConfirmacionForm(request.POST)
        if form.is_valid():
            confirmacion = form.save()

            mensaje = (
                f"Nueva confirmación de asistencia — Cotorreo de Rancho\n\n"
                f"Nombre: {confirmacion.nombre}\n"
                f"Teléfono: {confirmacion.telefono}\n"
                f"Número de personas: {confirmacion.num_personas}\n"
                f"Nota: {confirmacion.nota or 'Sin nota'}\n"
                f"Fecha de confirmación: {confirmacion.fecha_confirmacion.strftime('%d/%m/%Y %H:%M')}\n"
            )

            # fail_silently=False a propósito: si el email falla, queremos
            # VER el error en consola, pero sin tumbar la respuesta al
            # usuario -- por eso va en un try/except y el redirect ocurre
            # pase lo que pase con el correo.
            try:
                send_mail(
                    subject=f'Nueva confirmación: {confirmacion.nombre} ({confirmacion.num_personas} personas)',
                    message=mensaje,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['supervisorheredia@gmail.com'],
                    fail_silently=False,
                )
            except Exception:
                logger.exception('Error enviando email de confirmación de asistencia')

            return redirect('asistencia_confirmada')
    else:
        form = ConfirmacionForm()

    # El contador suma num_personas de TODOS los registros, no cuenta filas.
    # Así, si alguien confirma "yo + 3 acompañantes", cuentan las 4 personas.
    
    total_asistentes = Confirmacion.objects.aggregate(total=Sum('num_personas'))['total'] or 0
    total_asistentes= max(total_asistentes,81)
    # URL absoluta de la imagen para que las meta tags Open Graph/Twitter
    # funcionen al compartir el link (WhatsApp, Facebook, etc. necesitan la
    # URL completa, no la ruta relativa que genera {% static %}).
    imagen_absoluta = request.build_absolute_uri('/static/images/imagen.webp')

    return render(request, 'invitacion_emanuel.html', {
        'form': form,
        'total_asistentes': total_asistentes,
        'imagen_absoluta': imagen_absoluta,
    })


def asistencia_confirmada(request):
    return render(request, 'asistencia_confirmada.html')






import logging

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Sum

from .models import ConfirmacionBash
from .forms import ConfirmacionBashForm

logger = logging.getLogger(__name__)

HOST_EMAIL = 'rickwashburn23@gmail.com'


def bash_invitacion(request):
    if request.method == 'POST':
        form = ConfirmacionBashForm(request.POST)
        if form.is_valid():
            confirmacion = form.save()

            # ---- Email al anfitrión (Rick) ----
            mensaje_host = (
                f"New RSVP — PV End of Summer Bash\n\n"
                f"Name: {confirmacion.nombre}\n"
                f"Email: {confirmacion.email}\n"
                f"Phone: {confirmacion.telefono or 'Not provided'}\n"
                f"Party size: {confirmacion.num_personas}\n"
                f"Dish assignment: {confirmacion.dish_assignment}\n"
                f"Notes: {confirmacion.nota or 'None'}\n"
                f"Confirmed on: {confirmacion.fecha_confirmacion.strftime('%m/%d/%Y %H:%M')}\n"
            )
            try:
                send_mail(
                    subject=f'New RSVP: {confirmacion.nombre} ({confirmacion.num_personas} guests)',
                    message=mensaje_host,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[HOST_EMAIL],
                    fail_silently=False,
                )
            except Exception:
                logger.exception('Error sending host notification email for Bash RSVP')

            # ---- Email de confirmación al invitado ----
            primer_nombre = confirmacion.nombre.split()[0]
            mensaje_guest = (
                f"Hi {primer_nombre},\n\n"
                f"You're all set for the PV End of Summer Bash on September 25, 2026, "
                f"5:00-10:00 PM at Casa Cuale!\n\n"
                f"Your party size: {confirmacion.num_personas}\n"
                f"What to bring: {confirmacion.dish_assignment}\n\n"
                f"Address: Cuautémoc 634, Cerro (on the Cuale river, Gringo Gulch)\n"
                f"Parking is limited and the street is tight — Uber or walking is recommended.\n\n"
                f"See you there!\nRick & Jay\n"
            )
            try:
                send_mail(
                    subject="You're confirmed! PV End of Summer Bash 🎉",
                    message=mensaje_guest,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[confirmacion.email],
                    fail_silently=False,
                )
            except Exception:
                logger.exception('Error sending guest confirmation email for Bash RSVP')

            return redirect('bash_confirmed')
    else:
        form = ConfirmacionBashForm()

    
    total_assis = Confirmacion.objects.aggregate(total=Sum('num_personas'))['total'] or 0
    total_assis= max(total_assis,36)
    imagen_absoluta = request.build_absolute_uri('/static/images/event-rick.webp')

    return render(request, 'invitacion_rick.html', {
        'form': form,
        'total_assis': total_assis,
        'imagen_absoluta': imagen_absoluta,
    })


def bash_asistencia_confirmada(request):
    return render(request, 'invitacion_rick_success.html')