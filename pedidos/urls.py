from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import *

router = DefaultRouter()
router.register(r'mesas', views.MesaViewSet)
router.register(r'productos', views.ProductoViewSet)
router.register(r'pedidos', views.PedidoViewSet)
router.register(r'detalles', views.DetallePedidoViewSet)
router.register(r'empleados', views.EmpleadoViewSet)
router.register(r'history', views.OrderHistoryViewSet, basename='order-history')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/reports/', OrderReportView.as_view(), name='order-reports'),
    path('api/reports/category/', ProductCategoryReportView.as_view(), name='product-category-reports'),
    path('api/reports/product/', ProductNameReportView.as_view(), name='product-name-reports'),
]