import os
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from .models import Proyecto
from .utils import optimize_image


# ─── Helpers ────────────────────────────────────────────────────────────────

def _delete_file(field):
    try:
        if field and field.name:
            path = field.path
            if os.path.isfile(path):
                os.remove(path)
                # Si la carpeta del proyecto queda vacía, la limpiamos también
                folder = os.path.dirname(path)
                if os.path.isdir(folder) and not os.listdir(folder):
                    os.rmdir(folder)
    except (ValueError, FileNotFoundError, NotImplementedError):
        pass


def _replace_old_image(old_instance, new_instance, field_name):
    old_field = getattr(old_instance, field_name)
    new_field = getattr(new_instance, field_name)
    old_name  = old_field.name if old_field else None
    new_name  = new_field.name if new_field else None
    if old_name and old_name != new_name:
        _delete_file(old_field)


# ─── Proyecto ───────────────────────────────────────────────────────────────

@receiver(post_delete, sender=Proyecto)
def delete_proyecto_image(sender, instance, **kwargs):
    """Al eliminar el proyecto desde el admin, borra su imagen física."""
    _delete_file(instance.imagen)


@receiver(pre_save, sender=Proyecto)
def replace_proyecto_image(sender, instance, **kwargs):
    """Al editar y subir otra imagen, borra la anterior antes de guardar la nueva."""
    if not instance.pk:
        return
    try:
        old = Proyecto.objects.get(pk=instance.pk)
    except Proyecto.DoesNotExist:
        return
    _replace_old_image(old, instance, 'imagen')


@receiver(post_save, sender=Proyecto)
def optimize_proyecto_image(sender, instance, **kwargs):
    """Convierte automáticamente la imagen subida a WebP optimizado."""
    new_name = optimize_image(instance.imagen, max_width=1200, quality=80)
    if new_name:
        Proyecto.objects.filter(pk=instance.pk).update(imagen=new_name)