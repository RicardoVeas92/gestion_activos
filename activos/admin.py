from django.contrib import admin
from .models import (
    ImpresoraInstalada,
    ItemInventario,
    ModeloImpresora,
    RegistroUsoActivo,
)


@admin.register(ModeloImpresora)
class ModeloImpresoraAdmin(admin.ModelAdmin):
    list_display = ('marca', 'modelo', 'tecnologia', 'manual_pdf')
    search_fields = ('marca', 'modelo')


@admin.register(ImpresoraInstalada)
class ImpresoraInstaladaAdmin(admin.ModelAdmin):
    list_display = ('numero_serie', 'modelo', 'oficina', 'ubicacion')
    list_filter = ('modelo',)
    search_fields = ('numero_serie', 'oficina', 'ubicacion')


@admin.register(ItemInventario)
class ItemInventarioAdmin(admin.ModelAdmin):
    list_display = ('numero_parte', 'nombre', 'tipo', 'estado', 'imagen')
    list_filter = ('tipo', 'estado')
    search_fields = ('numero_parte', 'nombre')


@admin.register(RegistroUsoActivo)
class RegistroUsoActivoAdmin(admin.ModelAdmin):
    list_display = (
        'ticket_santiago',
        'impresora_instalada',
        'item_utilizado',
        'fecha_uso',
        'tecnico',
    )
    list_filter = ('fecha_uso',)
    search_fields = (
        'ticket_santiago',
        'impresora_instalada__numero_serie',
        'impresora_instalada__oficina',
    )