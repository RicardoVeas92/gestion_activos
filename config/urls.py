from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from activos.api_views import ModeloImpresoraViewSet, ItemInventarioViewSet, RegistroUsoActivoViewSet

router = DefaultRouter()
router.register(r'api/modelos', ModeloImpresoraViewSet)
router.register(r'api/inventario', ItemInventarioViewSet)
router.register(r'api/usos', RegistroUsoActivoViewSet)

# Personalización del diseño de Swagger
class CustomSwaggerView(SpectacularSwaggerView):
    custom_css = """
        .swagger-ui .topbar { background-color: #1a252f !important; }
        .swagger-ui .info .title { color: #2c3e50 !important; font-family: sans-serif; }
        .swagger-ui .scheme-container { background-color: #f8f9fa !important; }
        .swagger-ui { background-color: #ffffff; }
    """
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('activos.urls')),
    
    # API REST
    path('', include(router.urls)),
    
    # JWT Auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Swagger UI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )