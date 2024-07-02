from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'ordenes', views.OrdenDeReparacionViewSet, basename='ordenes')
router.register(r'presupuestos', views.PresupuestoSerializerViewSet, basename='presupuestos')
urlpatterns = [
    path('', include(router.urls )),
    path('api-auth/', include('rest_framework.urls'), name="rest_framework") # incluye las urls de django autenthications para el framework rest
]