from rest_framework import serializers
from web.models import OrdenDeReparacion, Cliente, Maquina, Presupuesto


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class MaquinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maquina
        fields = '__all__'

class OrdenDeReparacionSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer()
    maquina = MaquinaSerializer()

    class Meta:
        model = OrdenDeReparacion
        fields = '__all__'

class PresupuestoSerializer(serializers.ModelSerializer):
    orden = OrdenDeReparacionSerializer()
    class Meta:
        model = Presupuesto
        fields = '__all__'