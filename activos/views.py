from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Importaciones ajustadas a tus modelos reales
from .models import ModeloImpresora, ImpresoraInstalada, ItemInventario, RegistroUsoActivo
from .forms import ModeloImpresoraForm, ImpresoraInstaladaForm, ItemInventarioForm, CrearUsuarioForm, EditarUsuarioForm, RegistroUsoActivoForm


# ==========================================
# 1. AUTENTICACIÓN (LOGIN Y LOGOUT)
# ==========================================
def login_view(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    if request.method == 'POST':
        user_input = request.POST.get('username')
        pass_input = request.POST.get('password')
        user = authenticate(request, username=user_input, password=pass_input)

        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido de nuevo, {user.first_name or user.username}!')
            next_url = request.GET.get('next', 'inicio')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos. Intenta de nuevo.')

    return render(request, 'activos/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('login')


# ==========================================
# 2. DASHBOARD / INICIO
# ==========================================
@login_required
def inicio(request):
    total_modelos = ModeloImpresora.objects.count()
    total_instaladas = ImpresoraInstalada.objects.count()
    total_stock = ItemInventario.objects.filter(estado='DISPONIBLE').count()

    return render(request, 'activos/inicio.html', {
        'total_modelos': total_modelos,
        'total_instaladas': total_instaladas,
        'total_stock': total_stock,
    })


# ==========================================
# 3. MÓDULO MODELOS DE IMPRESORAS
# ==========================================
@login_required
def lista_modelos(request):
    query = request.GET.get('q', '')
    if query:
        modelos = ModeloImpresora.objects.filter(
            modelo__icontains=query
        ) | ModeloImpresora.objects.filter(
            marca__icontains=query
        )
    else:
        modelos = ModeloImpresora.objects.all()
    return render(request, 'activos/lista_modelos.html', {'modelos': modelos, 'query': query})


@login_required
def crear_modelo(request):
    if request.method == 'POST':
        form = ModeloImpresoraForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Modelo registrado correctamente.')
            return redirect('lista_modelos')
    else:
        form = ModeloImpresoraForm()
    return render(request, 'activos/form_modelo.html', {'form': form, 'titulo': 'Nuevo Modelo de Impresora'})


@login_required
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
    return render(request, 'activos/form_modelo.html', {'form': form, 'titulo': 'Editar Modelo de Impresora'})


@login_required
def eliminar_modelo(request, pk):
    modelo = get_object_or_404(ModeloImpresora, pk=pk)
    if request.method == 'POST':
        modelo.delete()
        messages.success(request, 'Modelo eliminado correctamente.')
        return redirect('lista_modelos')
    return render(request, 'activos/confirmar_eliminar.html', {'objeto': modelo, 'tipo': 'Modelo de Impresora', 'url_cancelar': 'lista_modelos'})


# ==========================================
# 4. MÓDULO IMPRESORAS INSTALADAS
# ==========================================
@login_required
def lista_impresoras(request):
    query = request.GET.get('q', '')
    if query:
        impresoras = ImpresoraInstalada.objects.filter(
            numero_serie__icontains=query
        ) | ImpresoraInstalada.objects.filter(
            oficina__icontains=query
        )
    else:
        impresoras = ImpresoraInstalada.objects.all()
    return render(request, 'activos/lista_impresoras.html', {'impresoras': impresoras, 'query': query})


@login_required
def crear_impresora(request):
    if request.method == 'POST':
        form = ImpresoraInstaladaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Impresora registrada con éxito.')
            return redirect('lista_impresoras')
    else:
        form = ImpresoraInstaladaForm()
    return render(request, 'activos/form_impresora.html', {'form': form, 'titulo': 'Nueva Impresora Instalada'})


@login_required
def editar_impresora(request, pk):
    impresora = get_object_or_404(ImpresoraInstalada, pk=pk)
    if request.method == 'POST':
        form = ImpresoraInstaladaForm(request.POST, instance=impresora)
        if form.is_valid():
            form.save()
            messages.success(request, 'Impresora actualizada correctamente.')
            return redirect('lista_impresoras')
    else:
        form = ImpresoraInstaladaForm(instance=impresora)
    return render(request, 'activos/form_impresora.html', {'form': form, 'titulo': 'Editar Impresora Instalada'})


@login_required
def eliminar_impresora(request, pk):
    impresora = get_object_or_404(ImpresoraInstalada, pk=pk)
    if request.method == 'POST':
        impresora.delete()
        messages.success(request, 'Impresora eliminada correctamente.')
        return redirect('lista_impresoras')
    return render(request, 'activos/confirmar_eliminar.html', {'objeto': impresora, 'tipo': 'Impresora Instalada', 'url_cancelar': 'lista_impresoras'})


# ==========================================
# 5. MÓDULO INVENTARIO / STOCK REPUESTOS
# ==========================================
@login_required
def lista_inventario(request):
    query = request.GET.get('q', '')
    if query:
        items = ItemInventario.objects.filter(
            numero_parte__icontains=query
        ) | ItemInventario.objects.filter(
            nombre__icontains=query
        )
    else:
        items = ItemInventario.objects.all()
    return render(request, 'activos/lista_inventario.html', {'items': items, 'query': query})


@login_required
def crear_item(request):
    if request.method == 'POST':
        form = ItemInventarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ítem agregado al stock correctamente.')
            return redirect('lista_inventario')
    else:
        form = ItemInventarioForm()
    return render(request, 'activos/form_item.html', {'form': form, 'titulo': 'Agregar Ítem a Stock'})


@login_required
def editar_item(request, pk):
    item = get_object_or_404(ItemInventario, pk=pk)
    if request.method == 'POST':
        form = ItemInventarioForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ítem actualizado correctamente.')
            return redirect('lista_inventario')
    else:
        form = ItemInventarioForm(instance=item)
    return render(request, 'activos/form_item.html', {'form': form, 'titulo': 'Editar Ítem de Inventario'})


@login_required
def eliminar_item(request, pk):
    item = get_object_or_404(ItemInventario, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Ítem eliminado del inventario.')
        return redirect('lista_inventario')
    return render(request, 'activos/confirmar_eliminar.html', {'objeto': item, 'tipo': 'Ítem de Inventario', 'url_cancelar': 'lista_inventario'})


# ==========================================
#6 MÓDULO REGISTRO DE SALIDAS / USOS POR TICKET
# ==========================================
@login_required
def lista_usos(request):
    usos = RegistroUsoActivo.objects.select_related('impresora_instalada', 'item_utilizado').all().order_by('-fecha_uso')
    return render(request, 'activos/lista_usos.html', {'usos': usos})


@login_required
def registrar_salida(request):
    if request.method == 'POST':
        form = RegistroUsoActivoForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            
            # Si el técnico no se escribió manualmente, asignar el usuario en sesión
            if not registro.tecnico:
                registro.tecnico = f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
            
            registro.save()

            # Actualizamos el estado del ítem de inventario a INSTALADO
            item = registro.item_utilizado
            item.estado = 'INSTALADO'
            item.save()

            messages.success(request, f'Salida registrada con éxito para el Ticket {registro.ticket_santiago}.')
            return redirect('lista_usos')
    else:
        form = RegistroUsoActivoForm()

    return render(request, 'activos/form_uso.html', {
        'form': form, 
        'titulo': 'Registrar Salida de Repuesto por Ticket'
    })


# ==========================================
# 7. MÓDULO EXCLUSIVO ADMIN: CREAR Y VER USUARIOS
# ==========================================
@login_required
def lista_usuarios(request):
    # Restricción: Si el usuario NO es admin, lo redirigimos al inicio
    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos de administrador para acceder a esta sección.')
        return redirect('inicio')

    usuarios = User.objects.all().order_by('-date_joined')
    return render(request, 'activos/lista_usuarios.html', {'usuarios': usuarios})


@login_required
def crear_usuario(request):
    # Restricción: Solo Administradores pueden crear usuarios
    if not request.user.is_staff:
        messages.error(request, 'Acceso denegado. Solo administradores pueden crear técnicos.')
        return redirect('inicio')

    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            nuevo_usuario = form.save(commit=False)
            # Encriptamos la contraseña adecuadamente
            nuevo_usuario.set_password(form.cleaned_data['password'])
            
            # Asignamos rango de Admin/Staff si el checkbox se marcó
            if form.cleaned_data.get('es_admin'):
                nuevo_usuario.is_staff = True
                nuevo_usuario.is_superuser = True
            
            nuevo_usuario.save()
            messages.success(request, f'Usuario "{nuevo_usuario.username}" creado exitosamente.')
            return redirect('lista_usuarios')
    else:
        form = CrearUsuarioForm()

    return render(request, 'activos/form_usuario.html', {'form': form, 'titulo': 'Registrar Nuevo Técnico / Admin'})

# Asegúrate de incluir EditarUsuarioForm en las importaciones al inicio de views.py:
# from .forms import ModeloImpresoraForm, ImpresoraInstaladaForm, ItemInventarioForm, CrearUsuarioForm, EditarUsuarioForm

# ==========================================
# EDITAR Y ELIMINAR USUARIOS (SOLO ADMIN)
# ==========================================
@login_required
def editar_usuario(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Acceso denegado. Solo administradores pueden editar usuarios.')
        return redirect('inicio')

    usuario_obj = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, instance=usuario_obj)
        if form.is_valid():
            usr = form.save(commit=False)
            es_admin = form.cleaned_data.get('es_admin')
            usr.is_staff = es_admin
            usr.is_superuser = es_admin
            usr.save()
            messages.success(request, f'Usuario "{usr.username}" actualizado correctamente.')
            return redirect('lista_usuarios')
    else:
        initial_data = {'es_admin': usuario_obj.is_staff}
        form = EditarUsuarioForm(instance=usuario_obj, initial=initial_data)

    return render(request, 'activos/form_usuario.html', {
        'form': form, 
        'titulo': f'Editar Usuario: {usuario_obj.username}'
    })


@login_required
def eliminar_usuario(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Acceso denegado. Solo administradores pueden eliminar usuarios.')
        return redirect('inicio')

    usuario_obj = get_object_or_404(User, pk=pk)

    # Protección: evitar que el administrador se elimine a sí mismo
    if usuario_obj == request.user:
        messages.error(request, 'No puedes eliminar tu propia cuenta de usuario en sesión.')
        return redirect('lista_usuarios')

    if request.method == 'POST':
        nombre_usr = usuario_obj.username
        usuario_obj.delete()
        messages.success(request, f'Usuario "{nombre_usr}" eliminado del sistema.')
        return redirect('lista_usuarios')

    return render(request, 'activos/confirmar_eliminar.html', {
        'objeto': usuario_obj.username, 
        'tipo': 'Usuario', 
        'url_cancelar': 'lista_usuarios'
    })