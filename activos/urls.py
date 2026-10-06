from django.urls import path
from . import views

urlpatterns = [
    # 0. Página Principal / Dashboard Tecnológico
    path('', views.inicio, name='inicio'),

    # 1. Modelos de Impresoras
    path('modelos/', views.lista_modelos, name='lista_modelos'),
    path('modelos/nuevo/', views.crear_modelo, name='crear_modelo'),
    path('modelos/editar/<int:pk>/', views.editar_modelo, name='editar_modelo'),
    path('modelos/eliminar/<int:pk>/', views.eliminar_modelo, name='eliminar_modelo'),

    # 2. Impresoras Instaladas
    path('impresoras/', views.lista_impresoras, name='lista_impresoras'),
    path('impresoras/nueva/', views.crear_impresora, name='crear_impresora'),
    path('impresoras/editar/<int:pk>/', views.editar_impresora, name='editar_impresora'),
    path('impresoras/eliminar/<int:pk>/', views.eliminar_impresora, name='eliminar_impresora'),

    # 3. Stock e Inventario
    path('inventario/', views.lista_inventario, name='lista_inventario'),
    path('inventario/nuevo/', views.crear_item, name='crear_item'),
    path('inventario/editar/<int:pk>/', views.editar_item, name='editar_item'),
    path('inventario/eliminar/<int:pk>/', views.eliminar_item, name='eliminar_item'),

    # 4. Transacciones / Salidas de Stock
    path('usos/', views.lista_usos, name='lista_usos'),
    path('usos/nuevo/', views.registrar_salida, name='registrar_salida'),
]