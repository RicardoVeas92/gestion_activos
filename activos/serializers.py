from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ModeloImpresora, ItemInventario, RegistroUsoActivo

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser']

class ModeloImpresoraSerializer(serializers.ModelSerializer):
    imagen = serializers.ImageField(required=False, allow_null=True)
    manual_pdf = serializers.FileField(required=False, allow_null=True)

    
    class Meta:
        model = ModeloImpresora
        fields = '__all__'

class ItemInventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemInventario
        fields = '__all__'

class RegistroUsoActivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroUsoActivo
        fields = '__all__'