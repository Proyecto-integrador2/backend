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
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PedidoFilter
from django.db.models import Count, Q
from rest_framework.views import APIView

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
        return Pedido.objects.filter(Q(estado = "pendiente") | Q(estado = "en_preparacion")).order_by('fecha_hora')  # Solo pedidos pendientes o en preparación ordenados por fecha

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

class OrderHistoryViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PedidoFilter
    ordering_fields = ['fecha_hora', 'id_pedido']

class OrderReportView(APIView):
    # permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        # Agrupar pedidos por fecha y contar cuántos hay por cada una
        pedidos_por_fecha = Pedido.objects.values('fecha_hora__date').annotate(total=Count('id_pedido')).order_by('fecha_hora__date')

        # Preparar los datos para el gráfico
        labels = [pedido['fecha_hora__date'].strftime('%Y-%m-%d') for pedido in pedidos_por_fecha]
        datasets = [{
            'label': 'Número de pedidos',
            'data': [pedido['total'] for pedido in pedidos_por_fecha],
            'borderColor': 'rgba(75, 192, 192, 1)',
            'backgroundColor': 'rgba(75, 192, 192, 0.2)',
        }]

        return Response({
            'labels': labels,
            'datasets': datasets
        })

class ProductCategoryReportView(APIView):
    # permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        # Agrupar por categoría de producto y contar cuántos hay en cada categoría
        categorias_por_producto = DetallePedido.objects.values('producto__categoria').annotate(total=Count('id_detalle_pedido')).order_by('producto__categoria')

        # Preparar los datos para el gráfico
        labels = [categoria['producto__categoria'] for categoria in categorias_por_producto]
        datasets = [{
            'label': 'Número de pedidos por categoría',
            'data': [categoria['total'] for categoria in categorias_por_producto],
            'borderColor': 'rgba(75, 192, 192, 1)',
            'backgroundColor': 'rgba(75, 192, 192, 0.2)',
        }]

        return Response({
            'labels': labels,
            'datasets': datasets
        })

class ProductNameReportView(APIView):
    # permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        # Agrupar por nombre de producto y contar cuántos hay en cada nombre
        productos_por_nombre = DetallePedido.objects.values('producto__nombre').annotate(total=Count('id_detalle_pedido')).order_by('producto__nombre')

        # Preparar los datos para el gráfico
        labels = [producto['producto__nombre'] for producto in productos_por_nombre]
        datasets = [{
            'label': 'Número de pedidos por producto',
            'data': [producto['total'] for producto in productos_por_nombre],
            'borderColor': 'rgba(153, 102, 255, 1)',
            'backgroundColor': 'rgba(153, 102, 255, 0.2)',
        }]

        return Response({
            'labels': labels,
            'datasets': datasets
        })