from django import forms

from activos.models import (
    ImpresoraInstalada,
    ItemInventario,
    ModeloImpresora,
    RegistroUsoActivo,
)


class ModeloImpresoraForm(forms.ModelForm):
    # Definimos explícitamente las opciones para que el desplegable siempre tenga datos
    OPCIONES_TECNOLOGIA = [
        ('Laser', 'Laser'),
        ('Inyección de tinta', 'Inyección de tinta'),
        ('Matricial', 'Matricial'),
        ('Térmica', 'Térmica'),
    ]

    tecnologia = forms.ChoiceField(
        choices=OPCIONES_TECNOLOGIA,
        widget=forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
        label='Tecnología'
    )

    class Meta:
        model = ModeloImpresora
        fields = ['marca', 'modelo', 'tecnologia', 'imagen', 'manual_pdf']
        widgets = {
            'marca': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'manual_pdf': forms.FileInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
        }


class ImpresoraInstaladaForm(forms.ModelForm):
    class Meta:
        model = ImpresoraInstalada
        fields = ['numero_serie', 'modelo', 'oficina', 'ubicacion']
        widgets = {
            'numero_serie': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'modelo': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
            'oficina': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
        }


# 2. FORMULARIO INVENTARIO / STOCK DE REPUESTOS
class ItemInventarioForm(forms.ModelForm):
    OPCIONES_TIPO = [
        ('SUMINISTRO', 'Suministro / Toner'),
        ('REPUESTO', 'Repuesto / Pieza'),
    ]

    OPCIONES_ESTADO = [
        ('DISPONIBLE', 'Disponible'),
        ('INSTALADO', 'Instalado / Usado'),
        ('DEFECTUOSO', 'Defectuoso / Dado de baja'),
    ]

    tipo = forms.ChoiceField(
        choices=OPCIONES_TIPO,
        widget=forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
        label='Tipo de Ítem'
    )

    estado = forms.ChoiceField(
        choices=OPCIONES_ESTADO,
        widget=forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
        label='Estado de Stock'
    )

    class Meta:
        model = ItemInventario
        fields = ['numero_parte', 'nombre', 'tipo', 'estado', 'imagen']
        widgets = {
            'numero_parte': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
        }


class RegistroUsoActivoForm(forms.ModelForm):

    class Meta:
        model = RegistroUsoActivo
        fields = [
            'ticket_santiago',
            'impresora_instalada',
            'item_utilizado',
            'tecnico',
            'observaciones',
        ]
        widgets = {
            'ticket_santiago': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: ST-2026-99'}
            ),
            'impresora_instalada': forms.Select(attrs={'class': 'form-select'}),
            'item_utilizado': forms.Select(attrs={'class': 'form-select'}),
            'tecnico': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item_utilizado'].queryset = ItemInventario.objects.filter(
            estado='DISPONIBLE'
        )