from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import NewsletterSubscription,ContactMessage

@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')  # Customize columns to display
    search_fields = ('email',)  # Optional: Add search functionality





@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display  = ['name', 'email', 'phone', 'created_at', 'read']
    list_filter   = ['read', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    actions = ['mark_as_read', 'mark_as_unread']

    fieldsets = (
        ('Contact Information', {'fields': ('name', 'email', 'phone')}),
        ('Message',             {'fields': ('message',)}),
        ('Status',              {'fields': ('read', 'created_at')}),
    )

    def mark_as_read(self, request, queryset):
        queryset.update(read=True)
    mark_as_read.short_description = "Mark selected messages as read"

    def mark_as_unread(self, request, queryset):
        queryset.update(read=False)
    mark_as_unread.short_description = "Mark selected messages as unread"





from django import forms
from django.contrib import admin
from django.utils.html import format_html
from .models import Proyecto


class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = '__all__'
        widgets = {
            'color_acento': forms.TextInput(attrs={
                'placeholder': '#1f1f1f',
                'style': 'font-family: monospace;',
            }),
            'color_texto': forms.TextInput(attrs={
                'placeholder': '#ffffff',
                'style': 'font-family: monospace;',
            }),
        }


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    form = ProyectoForm
    list_display  = ('dominio', 'categoria', 'color_preview', 'orden', 'destacado', 'activo')
    list_editable = ('orden', 'destacado', 'activo')
    list_filter   = ('categoria', 'activo', 'destacado')
    search_fields = ('nombre', 'dominio', 'descripcion')
    fieldsets = (
        ('Información General', {
            'fields': ('nombre', 'dominio', 'url', 'categoria')
        }),
        ('Contenido', {
            'fields': ('descripcion', 'imagen','bandera_pais')
        }),
        ('Colores', {
            'fields': ('color_acento', 'color_texto'),
            'description': 'Pega el código hexadecimal del color, ej: #1f1f1f. Este color se usa tanto en el borde superior de la tarjeta como en el fondo del badge de categoría.'
        }),
        ('Visibilidad', {
            'fields': ('orden', 'destacado', 'activo')
        }),
    )

    def color_preview(self, obj):
        return format_html(
            '<span style="display:inline-block;width:20px;height:20px;border-radius:4px;'
            'background:{};border:1px solid #999;"></span>',
            obj.color_acento
        )
    color_preview.short_description = 'Color'







from django.contrib import admin, messages
from django.db.models import Sum
from .models import Confirmacion


@admin.register(Confirmacion)
class ConfirmacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'num_personas', 'tiene_nota', 'fecha_confirmacion')
    list_filter = ('fecha_confirmacion',)
    search_fields = ('nombre', 'telefono', 'nota')
    ordering = ('-fecha_confirmacion',)
    readonly_fields = ('fecha_confirmacion',)

    fieldsets = (
        ('Datos del invitado', {
            'fields': ('nombre', 'telefono', 'num_personas', 'nota')
        }),
        ('Registro', {
            'fields': ('fecha_confirmacion',)
        }),
    )

    def tiene_nota(self, obj):
        return bool(obj.nota)
    tiene_nota.boolean = True
    tiene_nota.short_description = 'Nota'

    def changelist_view(self, request, extra_context=None):
        # Muestra el total real de personas confirmadas como un mensaje
        # informativo arriba de la tabla — no cuenta filas, suma num_personas
        # de todas las confirmaciones. No requiere un template personalizado.
        total_personas = Confirmacion.objects.aggregate(total=Sum('num_personas'))['total'] or 0
        total_confirmaciones = Confirmacion.objects.count()
        messages.info(
            request,
            f'📊 Total: {total_personas} personas confirmadas en {total_confirmaciones} '
            f'confirmación{"es" if total_confirmaciones != 1 else ""}.'
        )
        return super().changelist_view(request, extra_context=extra_context)

    






from django.contrib import admin, messages
from django.db.models import Sum
from .models import ConfirmacionBash


@admin.register(ConfirmacionBash)
class ConfirmacionBashAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'telefono', 'num_personas', 'dish_assignment', 'fecha_confirmacion')
    list_filter = ('fecha_confirmacion',)
    search_fields = ('nombre', 'email', 'telefono', 'nota')
    ordering = ('-fecha_confirmacion',)
    readonly_fields = ('fecha_confirmacion', 'dish_assignment')

    fieldsets = (
        ('Guest Info', {
            'fields': ('nombre', 'email', 'telefono', 'num_personas', 'nota')
        }),
        ('Assignment & Record', {
            'fields': ('dish_assignment', 'fecha_confirmacion')
        }),
    )

    def changelist_view(self, request, extra_context=None):
        total_personas = ConfirmacionBash.objects.aggregate(total=Sum('num_personas'))['total'] or 0
        total_confirmaciones = ConfirmacionBash.objects.count()
        messages.info(
            request,
            f'🎉 Total: {total_personas} guests confirmed across {total_confirmaciones} RSVP'
            f'{"s" if total_confirmaciones != 1 else ""}.'
        )
        return super().changelist_view(request, extra_context=extra_context)