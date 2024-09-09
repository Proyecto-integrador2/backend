from django.shortcuts import render
from rest_framework import viewsets
from .models import Mesa, Producto, Pedido, DetallePedido, Empleado
from .serializers import MesaSerializer, ProductoSerializer, PedidoSerializer, DetallePedidoSerializer, EmpleadoSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
class MesaViewSet(viewsets.ModelViewSet):
    queryset = Mesa.objects.all()
    serializer_class = MesaSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    def get(self, request):
        return Response({"message": "Solo administradores pueden acceder a esta vista"})

class DetallePedidoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer

    def get(self, request):
        return Response({"message": "Solo administradores pueden acceder a esta vista"})

class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer

