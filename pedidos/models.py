from django.db import models

class Mesa(models.Model):
    id_mesa = models.AutoField(primary_key=True)
    ubicacion = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Mesa {self.id_mesa} - {self.ubicacion if self.ubicacion else 'Sin ubicación'}"


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    categoria = models.TextField()
    ingredientes = models.JSONField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen_url = models.URLField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_preparacion', 'En preparación'),
        ('entregado', 'Entregado'),
    ]

    id_pedido = models.AutoField(primary_key=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE, related_name='pedidos')

    def __str__(self):
        return f"Pedido {self.id_pedido} - Mesa {self.mesa.id_mesa}"


class DetallePedido(models.Model):
    id_detalle_pedido = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    comentarios = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Detalle {self.id_detalle_pedido} - Pedido {self.pedido.id_pedido}"


class Empleado(models.Model):
    ROL_CHOICES = [
        ('mesero', 'Mesero'),
        ('bartender', 'Bartender'),
    ]

    id_empleado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, null=True, blank=True, related_name='empleados')

    def __str__(self):
        return f"Empleado {self.nombre} - {self.rol}"