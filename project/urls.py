from django.contrib import admin
from django.urls import path
from crisapp import views
from . import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),

    # Home — dos paths, mismo name está bien para Django
    path('',        views.home, name='inicio'),
    path('inicio/', views.home, name='inicio'),

    # Contacto
    path('enviar_email/', views.send_email, name='enviar_email'),

    # Newsletter
    path('subscribe/', views.suscribirse, name='subscribe'),

    # Páginas estáticas
    path('politica_privacidad/',  views.politica_privacidad,  name='politica_privacidad'),
    path('terminos_condiciones/', views.terminos_condiciones, name='terminos_condiciones'),
    path('about_us/',             views.about_us,             name='about_us'),
    path('carta_recomendacion/',  views.carta_silvia,         name='carta_recomendacion'),

    # Herramientas
    path('generar_qr/',         views.generar_qr,          name='generar_qr'),
    path('convertir-imagenes/', views.convertir_imagenes,  name='convertir_imagenes'),
    path('video-a-gif/',        views.convertir_video_gif, name='convertir_video_gif'),
    path('quitar-fondo/',       views.quitar_fondo,        name='quitar_fondo'),
    path('aplicar-fondo/',      views.aplicar_fondo,       name='aplicar_fondo'),



    # ... tus rutas existentes ...
    path('invitacion/', views.invitacion, name='invitacion'),
    path('asistencia-confirmada/', views.asistencia_confirmada, name='asistencia_confirmada'),


    path('bash_invitation/', views.bash_invitacion, name='bash_invitation'),
    path('bash-confirmed/', views.bash_asistencia_confirmada, name='bash_confirmed'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




