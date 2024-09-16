# filters.py

import django_filters
from .models import Pedido

class PedidoFilter(django_filters.FilterSet):
    fecha_hora_year = django_filters.NumberFilter(field_name='fecha_hora', lookup_expr='year')
    fecha_hora_month = django_filters.NumberFilter(field_name='fecha_hora', lookup_expr='month')
    fecha_hora_day = django_filters.NumberFilter(field_name='fecha_hora', lookup_expr='day')

    class Meta:
        model = Pedido
        fields = ['mesa__ubicacion', 'estado', 'fecha_hora_year', 'fecha_hora_month', 'fecha_hora_day']
