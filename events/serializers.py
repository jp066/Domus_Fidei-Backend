from rest_framework import serializers
from .models import (
    RetiroAcampamento, EquipeRetiro, 
    ServoRetiro, CronogramaRetiro, 
    InscricaoRetiro, Eventos,
    Formacoes, AssembleiaParoquial
)

class EventosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eventos
        fields = ['nome_evento', 'descricao', 'data_inicio', 'data_fim', 'local']
        read_only_fields = ('id', 'created_at', 'updated_at')

    def create(self, validated_data):
        coordenador = self.context['coordenador'] # Obtém o coordenador do contexto que foi passado na view
        return Eventos.objects.create(coordenador=coordenador, **validated_data) # Cria um novo evento com os dados validados e o coordenador associado


    def update(self, instance, validated_data):
        for attr, value in validated_data.items(): # para cada atributo e valor nos dados validados
            setattr(instance, attr, value) # define o atributo do instance com o valor
        instance.save() # salva a instância atualizada
        return instance # retorna a instância atualizada
    

class DesativarEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eventos
        fields = ['ativo']
        read_only_fields = ('id', 'created_at', 'updated_at')

    def update(self, instance, validated_data):
        instance.ativo = False  # Define o campo ativo como False
        instance.save()  # Salva a instância atualizada
        return instance  # Retorna a instância atualizada