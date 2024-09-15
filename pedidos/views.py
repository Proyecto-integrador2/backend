from django.shortcuts import render
from rest_framework import viewsets
from .models import Mesa, Producto, Pedido, DetallePedido, Empleado
from .serializers import MesaSerializer, ProductoSerializer, PedidoSerializer, PedidoCreateSerializer, \
    DetallePedidoSerializer, EmpleadoSerializer, DetallePedidoCreateSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your views here.
class MesaViewSet(viewsets.ModelViewSet):
    queryset = Mesa.objects.all()
    serializer_class = MesaSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAdminUser]
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    def get_queryset(self):
        return Pedido.objects.filter(estado='pendiente').order_by('fecha_hora')  # Solo pedidos pendientes ordenados por fecha

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        detalles_data = data.pop('detalles', [])
        pedido_serializer = PedidoCreateSerializer(data=data)

        if pedido_serializer.is_valid():
            pedido = pedido_serializer.save()
            for detalle_data in detalles_data:
                detalle_data['pedido'] = pedido.id_pedido
                detalle_serializer = DetallePedidoCreateSerializer(data=detalle_data)
                if detalle_serializer.is_valid():
                    detalle_serializer.save()
                else:
                    return Response(detalle_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Enviar notificación por WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'pedidos',
                {
                    'type': 'send_notification',
                    'message': f'Nuevo pedido: {pedido.mesa}'
                }
            )
            return Response(pedido_serializer.data, status=status.HTTP_201_CREATED)
        return Response(pedido_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DetallePedidoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer

    def get(self, request):
        return Response({"message": "Solo administradores pueden acceder a esta vista"})

class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer

