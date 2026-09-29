from django import forms
from django.core.validators import RegexValidator
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3

SPAM_KEYWORDS = [
    'viagra', 'casino', 'lottery', 'click here', 'buy now', 'bitcoin',
    'crypto', 'seo', 'search engine', 'ranking', 'web traffic', 'backlinks',
    'make money', 'work from home', 'earn $', 't.me/', 'http://',
]


class ContactForm(forms.Form):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)
    captcha = ReCaptchaField(
        widget=ReCaptchaV3(attrs={'required_score': 0.5, 'action': 'contact'}),
        label='',
        error_messages={
            'required': 'Por favor completa la verificación de seguridad.',
            'invalid':  'La verificación de seguridad falló. Por favor intenta nuevamente.'
        }
    )
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Juan Pérez',
            'class': 'form-control',
        }),
        label='Nombre Completo'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'tu.email@ejemplo.com',
            'class': 'form-control',
        }),
        label='Correo Electrónico'
    )
    phone = forms.CharField(
        max_length=15,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="El teléfono debe tener el formato: '+999999999'. Hasta 15 dígitos."
        )],
        widget=forms.TextInput(attrs={
            'placeholder': '+52 123 456 7890',
            'class': 'form-control',
        }),
        label='Teléfono'
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Por favor describe cómo podemos ayudarte...',
            'class': 'form-control',
            'rows': 6,
        }),
        label='Mensaje'
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('honeypot'):
            raise forms.ValidationError('Bot detected.')
        message = cleaned_data.get('message', '')
        if any(kw in message.lower() for kw in SPAM_KEYWORDS):
            raise forms.ValidationError('Tu mensaje contiene contenido sospechoso.')
        return cleaned_data


from .models import Subscriber

class SubscriberForm(forms.ModelForm):
    # Sin captcha — el honeypot en el template es suficiente protección
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Subscriber
        fields = ['nombre', 'email']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@email.com',
            })
        }
        labels = {
            'nombre': 'Name',
            'email':  'Email'
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('honeypot'):
            raise forms.ValidationError('Bot detected.')
        return cleaned_data 





from django import forms
from .models import Confirmacion


class ConfirmacionForm(forms.ModelForm):
    class Meta:
        model = Confirmacion
        fields = ['nombre', 'telefono', 'num_personas', 'nota']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Tu nombre completo',
                'required': True,
                'disabled': True,
            }),
            'telefono': forms.TextInput(attrs={
                'placeholder': '312 123 4567',
                'required': True,
                'disabled': True,
            }),
            'num_personas': forms.NumberInput(attrs={
                'min': 1,
                'value': 1,
                'required': True,
                'disabled': True,
            }),
            'nota': forms.Textarea(attrs={
                'placeholder': '¿Alguna nota especial? (opcional)',
                'rows': 3,
                'disabled': True,
            }),
        }
    







from .models import ConfirmacionBash


class ConfirmacionBashForm(forms.ModelForm):
    class Meta:
        model = ConfirmacionBash
        fields = ['nombre', 'email', 'telefono', 'num_personas', 'nota']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Full name (first & last)', 'required': True}),
            'email': forms.EmailInput(attrs={'placeholder': 'you@email.com', 'required': True}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Phone (optional)'}),
            'num_personas': forms.NumberInput(attrs={'min': 1, 'value': 1, 'required': True}),
            'nota': forms.Textarea(attrs={'placeholder': 'Dietary restrictions or notes (optional)', 'rows': 3}),
        }
        labels = {
            'nombre': 'Full Name',
            'email': 'Email',
            'telefono': 'Phone Number',
            'num_personas': 'Number in Your Party',
            'nota': 'Notes',
        }

    def clean_num_personas(self):
        num = self.cleaned_data['num_personas']
        if num < 1:
            raise forms.ValidationError('Must be at least 1 person.')
        return num

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()
        if len(nombre.split()) < 2:
            raise forms.ValidationError('Please enter your first and last name (needed for the potluck assignment).')
        return nombre