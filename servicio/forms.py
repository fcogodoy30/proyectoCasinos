from django.forms import ModelForm
from .models import CasinoColacion

class colacionForm(ModelForm):
    class Meta:
        model = CasinoColacion
        fields = ['titulo','descripcion','fecha_servicio']