from django.urls import path
from . import views

urlpatterns = [
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Inicio / Dashboard
    path('', views.inicio, name='inicio'),

    # Módulo Modelos de Impresoras
    path('modelos/', views.lista_modelos, name='lista_modelos'),
    path('modelos/crear/', views.crear_modelo, name='crear_modelo'),
    path('modelos/editar/<int:pk>/', views.editar_modelo, name='editar_modelo'),
    path('modelos/eliminar/<int:pk>/', views.eliminar_modelo, name='eliminar_modelo'),

    # Módulo Impresoras Instaladas
    path('impresoras/', views.lista_impresoras, name='lista_impresoras'),
    path('impresoras/crear/', views.crear_impresora, name='crear_impresora'),
    path('impresoras/editar/<int:pk>/', views.editar_impresora, name='editar_impresora'),
    path('impresoras/eliminar/<int:pk>/', views.eliminar_impresora, name='eliminar_impresora'),

    # Módulo Inventario / Stock
    path('inventario/', views.lista_inventario, name='lista_inventario'),
    path('inventario/crear/', views.crear_item, name='crear_item'),
    path('inventario/editar/<int:pk>/', views.editar_item, name='editar_item'),
    path('inventario/eliminar/<int:pk>/', views.eliminar_item, name='eliminar_item'),

    # Módulo Salidas por Ticket
    path('salidas/', views.lista_usos, name='lista_usos'),
    path('salidas/registrar/', views.registrar_salida, name='registrar_salida'),

    # Módulo Exclusivo Admin: Usuarios
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:pk>/', views.eliminar_usuario, name='eliminar_usuario'),
]