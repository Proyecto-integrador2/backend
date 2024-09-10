from rest_framework import serializers
from .models import Mesa, Pedido, DetallePedido, Producto, Empleado

class MesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesa
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class DetallePedidoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    producto_imagen = serializers.CharField(source='producto.imagen_url', read_only=True)

    class Meta:
        model = DetallePedido
        fields = ['id_detalle_pedido', 'producto_nombre', 'cantidad', 'comentarios', 'producto_imagen']

class PedidoSerializer(serializers.ModelSerializer):
    detalles = DetallePedidoSerializer(many=True, read_only=True)  # Incluir detalles del pedido
    mesa_numero = serializers.CharField(source='mesa.id_mesa', read_only=True)
    mesa_ubicacion = serializers.CharField(source='mesa.ubicacion', read_only=True)

    class Meta:
        model = Pedido
        fields = ['id_pedido', 'fecha_hora', 'estado', 'mesa_numero', 'mesa_ubicacion', 'detalles']

class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = '__all__'