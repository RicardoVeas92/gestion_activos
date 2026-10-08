from rest_framework import viewsets, permissions
from .models import ModeloImpresora, ItemInventario, RegistroUsoActivo
from .serializers import ModeloImpresoraSerializer, ItemInventarioSerializer, RegistroUsoActivoSerializer

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class ModeloImpresoraViewSet(viewsets.ModelViewSet):
    queryset = ModeloImpresora.objects.all()
    serializer_class = ModeloImpresoraSerializer
    permission_classes = [IsAdminOrReadOnly]

class ItemInventarioViewSet(viewsets.ModelViewSet):
    queryset = ItemInventario.objects.all()
    serializer_class = ItemInventarioSerializer
    permission_classes = [IsAdminOrReadOnly]

class RegistroUsoActivoViewSet(viewsets.ModelViewSet):
    queryset = RegistroUsoActivo.objects.all()
    serializer_class = RegistroUsoActivoSerializer
    permission_classes = [permissions.IsAuthenticated]