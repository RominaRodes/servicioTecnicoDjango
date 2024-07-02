from django.shortcuts import render
from rest_framework import viewsets
from web.models import OrdenDeReparacion, Presupuesto
from api.serializers import OrdenDeReparacionSerializer, PresupuestoSerializer
from rest_framework import permissions

class OrdenDeReparacionViewSet(viewsets.ModelViewSet):
    queryset = OrdenDeReparacion.objects.all()
    serializer_class = OrdenDeReparacionSerializer

class PresupuestoSerializerViewSet(viewsets.ModelViewSet):
    queryset = Presupuesto.objects.all()
    serializer_class= PresupuestoSerializer