from django.db import models

# Create your models here.



class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email




class ContactMessage(models.Model):
    name       = models.CharField(max_length=200)
    email      = models.EmailField()
    phone      = models.CharField(max_length=20, blank=True)
    message    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read       = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d')}"
    


class Subscriber(models.Model):
    email             = models.EmailField(unique=True)
    nombre            = models.CharField(max_length=100)
    fecha_suscripcion = models.DateTimeField(auto_now_add=True)
    activo            = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} - {self.email}"

    class Meta:
        verbose_name        = "Subscriber"
        verbose_name_plural = "Subscribers"
        ordering            = ['-fecha_suscripcion']


def proyecto_image_path(instance, filename):
    """
    Carpeta fija por proyecto basada en el pk (igual que hero_image_path en
    Vallarta Limpio). Mientras el proyecto exista, cualquier imagen nueva que
    se suba al editar cae en la MISMA carpeta — no se crean carpetas extra en
    cada edición, solo en la primera creación (antes de tener pk).
    """
    folder = f'proyecto_{instance.pk}' if instance.pk else 'proyecto_new'
    return f'portafolio/{folder}/{filename}'


class Proyecto(models.Model):
    CATEGORIA_CHOICES = [
        ('hospedaje', 'Hospedaje y Reservaciones'),
        ('bienes-raices', 'Bienes Raíces'),
        ('restaurantes', 'Restaurantes y Pedidos'),
        ('tiendas', 'Tiendas en Línea'),
        ('ong', 'ONG y Fundaciones'),
        ('arte', 'Arte y Cultura'),
        ('servicios', 'Servicios Profesionales'),
        ('comunidades', 'Comunidades e Instituciones'),
    ]

    nombre      = models.CharField(max_length=100, help_text="Nombre del cliente/proyecto")
    dominio     = models.CharField(max_length=100, help_text="Ej: rentasruiz.com")
    url         = models.URLField(default="https://")
    descripcion = models.TextField()
    categoria   = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    imagen      = models.ImageField(upload_to=proyecto_image_path)
    bandera_pais = models.ImageField(upload_to=proyecto_image_path ,null=True,blank=True)
    color_acento = models.CharField(
        max_length=7, default='#00d9ff',
        help_text="Color del borde superior de la tarjeta y del fondo del badge de categoría. Ej: #00d9ff"
    )
    color_texto = models.CharField(
        max_length=7, default='#0a0a0a',
        help_text="Color del texto del badge de categoría (para que se lea bien sobre el color de acento)"
    )
    orden       = models.PositiveIntegerField(default=0, help_text="Menor número aparece primero")
    destacado   = models.BooleanField(default=False, help_text="Mostrar con mayor prioridad")
    activo      = models.BooleanField(default=True, help_text="Desmarcar para ocultar sin borrar")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['orden', '-destacado', '-fecha_creacion']
        verbose_name        = "Proyecto"
        verbose_name_plural = "Proyectos"

    def __str__(self):
        return self.dominio





class Confirmacion(models.Model):
    nombre = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20)
    # Aquí está la clave del contador: en vez de un BooleanField de "asiste
    # sí/no" (que solo contaría personas, no invitados con acompañantes),
    # guardamos cuántas personas trae cada confirmación. El contador real
    # es la SUMA de este campo en todos los registros, no el conteo de filas.
    num_personas = models.PositiveIntegerField(default=1)
    nota = models.TextField(blank=True)
    fecha_confirmacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_confirmacion']
        verbose_name = "Confirmación de asistencia"
        verbose_name_plural = "Confirmaciones de asistencia"

    def __str__(self):
        return f"{self.nombre} ({self.num_personas} persona{'s' if self.num_personas != 1 else ''})"

    


from django.db import models


class ConfirmacionBash(models.Model):
    """RSVP para el 'PV End of Summer Bash/Potluck' de Rick y Jay.
    Modelo independiente de Confirmacion (Cotorreo de Rancho) — ese evento
    sigue activo y no debe verse afectado por este."""

    nombre = models.CharField(max_length=150, help_text="Full name (first & last, needed for potluck assignment)")
    email = models.EmailField(help_text="Se usa para enviarle el email de confirmación al invitado")
    telefono = models.CharField(max_length=20, blank=True)
    num_personas = models.PositiveIntegerField(default=1)
    nota = models.TextField(blank=True, help_text="Dietary restrictions or notes")
    fecha_confirmacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_confirmacion']
        verbose_name = "RSVP — End of Summer Bash"
        verbose_name_plural = "RSVPs — End of Summer Bash"

    def __str__(self):
        return f"{self.nombre} ({self.num_personas})"

    @property
    def dish_assignment(self):
        """Asigna automáticamente el plato según la inicial del apellido,
        siguiendo la regla que dio el cliente (A-I / J-R / S-Z)."""
        partes = self.nombre.strip().split()
        apellido = partes[-1] if partes else ''
        inicial = apellido[0].upper() if apellido else ''

        if inicial in 'ABCDEFGHI':
            return 'Appetizer / Entrada'
        elif inicial in 'JKLMNOPQR':
            return 'Main or Side Dish / Plato Fuerte o Guarnición'
        elif inicial in 'STUVWXYZ':
            return 'Dessert / Postre'
        return 'Bring whatever you like!'