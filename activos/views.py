from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from forms import (
    ImpresoraInstaladaForm,
    ItemInventarioForm,
    ModeloImpresoraForm,
    RegistroUsoActivoForm,
)
from activos.models import (
    ImpresoraInstalada,
    ItemInventario,
    ModeloImpresora,
    RegistroUsoActivo,
)

# -------------------------------------------------------------------
# 1. VISTAS PARA MANTENEDOR DE MODELOS DE IMPRESORAS
# -------------------------------------------------------------------
def inicio(request):
    total_modelos = ModeloImpresora.objects.count()
    total_instaladas = ImpresoraInstalada.objects.count()
    total_stock = ItemInventario.objects.filter(estado='DISPONIBLE').count()
    total_salidas = RegistroUsoActivo.objects.count()

    context = {
        'total_modelos': total_modelos,
        'total_instaladas': total_instaladas,
        'total_stock': total_stock,
        'total_salidas': total_salidas,
    }
    return render(request, 'activos/inicio.html', context)

def lista_modelos(request):
    query = request.GET.get('q', '')
    if query:
        modelos = ModeloImpresora.objects.filter(
            Q(marca__icontains=query) | Q(modelo__icontains=query)
        )
    else:
        modelos = ModeloImpresora.objects.all()
    return render(request, 'activos/lista_modelos.html', {'modelos': modelos, 'query': query})

def crear_modelo(request):
    if request.method == 'POST':
        form = ModeloImpresoraForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Modelo de impresora registrado con éxito.')
            return redirect('lista_modelos')
    else:
        form = ModeloImpresoraForm()
    return render(request, 'activos/form_modelo.html', {'form': form, 'titulo': 'Registrar Nuevo Modelo'})

def editar_modelo(request, pk):
    modelo = get_object_or_404(ModeloImpresora, pk=pk)
    if request.method == 'POST':
        form = ModeloImpresoraForm(request.POST, request.FILES, instance=modelo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Modelo actualizado correctamente.')
            return redirect('lista_modelos')
    else:
        form = ModeloImpresoraForm(instance=modelo)
    return render(request, 'activos/form_modelo.html', {
        'form': form, 
        'titulo': 'Editar Modelo de Impresora'
    })

def eliminar_modelo(request, pk):
    modelo = get_object_or_404(ModeloImpresora, pk=pk)
    if request.method == 'POST':
        modelo.delete()
        messages.success(request, 'Modelo eliminado con éxito.')
        return redirect('lista_modelos')
    return render(request, 'activos/confirmar_eliminar.html', {'objeto': modelo, 'tipo': 'Modelo de Impresora'})


# -------------------------------------------------------------------
# 2. VISTAS PARA IMPRESORAS INSTALADAS (EN CLIENTES / OFICINAS)
# -------------------------------------------------------------------

def lista_impresoras(request):
    query = request.GET.get('q', '')
    if query:
        impresoras = ImpresoraInstalada.objects.filter(
            Q(numero_serie__icontains=query) | Q(oficina__icontains=query) | Q(modelo__modelo__icontains=query)
        )
    else:
        impresoras = ImpresoraInstalada.objects.all().select_related('modelo')
    return render(request, 'activos/lista_impresoras.html', {'impresoras': impresoras, 'query': query})

def crear_impresora(request):
    if request.method == 'POST':
        form = ImpresoraInstaladaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Impresora instalada registrada con éxito.')
            return redirect('lista_impresoras')
    else:
        form = ImpresoraInstaladaForm()
    return render(request, 'activos/form_impresora.html', {'form': form, 'titulo': 'Registrar Impresora Instalada'})

def editar_impresora(request, pk):
    impresora = get_object_or_404(ImpresoraInstalada, pk=pk)
    if request.method == 'POST':
        form = ImpresoraInstaladaForm(request.POST, instance=impresora)
        if form.is_valid():
            form.save()
            messages.success(request, 'Datos de la impresora actualizados correctamente.')
            return redirect('lista_impresoras')
    else:
        form = ImpresoraInstaladaForm(instance=impresora)
    return render(request, 'activos/form_impresora.html', {'form': form, 'titulo': 'Editar Impresora Instalada'})

def eliminar_impresora(request, pk):
    impresora = get_object_or_404(ImpresoraInstalada, pk=pk)
    if request.method == 'POST':
        impresora.delete()
        messages.success(request, 'Impresora instalada eliminada con éxito.')
        return redirect('lista_impresoras')
    return render(request, 'activos/confirmar_eliminar.html', {'objeto': impresora, 'tipo': 'Impresora Instalada'})


# -------------------------------------------------------------------
# 3. VISTAS PARA MANTENEDOR DE INVENTARIO (REPUESTOS Y SUMINISTROS)
# -------------------------------------------------------------------

def lista_inventario(request):
    query = request.GET.get('q', '')
    if query:
        items = ItemInventario.objects.filter(
            Q(numero_parte__icontains=query) | Q(nombre__icontains=query) | Q(tipo__icontains=query)
        )
    else:
        items = ItemInventario.objects.all()
    return render(request, 'activos/lista_inventario.html', {'items': items, 'query': query})

def crear_item(request):
    if request.method == 'POST':
        form = ItemInventarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ítem agregado al inventario con éxito.')
            return redirect('lista_inventario')
    else:
        form = ItemInventarioForm()
    return render(request, 'activos/form_item.html', {'form': form, 'titulo': 'Agregar Ítem a Stock'})

def editar_item(request, pk):
    item = get_object_or_404(ItemInventario, pk=pk)
    if request.method == 'POST':
        form = ItemInventarioForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ítem de inventario actualizado correctamente.')
            return redirect('lista_inventario')
    else:
        form = ItemInventarioForm(instance=item)
    return render(request, 'activos/form_item.html', {'form': form, 'titulo': 'Editar Ítem de Stock'})

def eliminar_item(request, pk):
    item = get_object_or_404(ItemInventario, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Ítem de inventario eliminado con éxito.')
        return redirect('lista_inventario')
    return render(request, 'activos/confirmar_eliminar.html', {'objeto': item, 'tipo': 'Ítem de Inventario'})


# -------------------------------------------------------------------
# 4. VISTAS PARA LA TRANSACCIÓN (SALIDAS / CONSUMO POR TICKET)
# -------------------------------------------------------------------

def lista_usos(request):
    query = request.GET.get('q', '')
    if query:
        usos = RegistroUsoActivo.objects.filter(
            Q(ticket_santiago__icontains=query) | Q(tecnico__icontains=query)
        )
    else:
        usos = RegistroUsoActivo.objects.all().select_related('impresora_instalada', 'item_utilizado')
    return render(request, 'activos/lista_usos.html', {'usos': usos, 'query': query})

def registrar_salida(request):
    if request.method == 'POST':
        form = RegistroUsoActivoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Salida de inventario y consumo registrados correctamente.')
            return redirect('lista_usos')
    else:
        form = RegistroUsoActivoForm()
    return render(request, 'activos/form_uso.html', {'form': form, 'titulo': 'Registrar Salida de Repuesto / Suministro'})
