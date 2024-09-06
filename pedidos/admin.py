from django.contrib import admin
from .models import Mesa, Producto, Pedido, DetallePedido, Empleado

admin.site.register(Mesa)
admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(Empleado)
