from rest_framework import serializers
from .models import (
    RetiroAcampamento, EquipeRetiro, 
    ServoRetiro, CronogramaRetiro, 
    InscricaoRetiro, Eventos,
    Formacoes, AssembleiaParoquial
)

class EventosSerializer(serializers.ModelSerializer):
    coordenador = serializers.SerializerMethodField() # obtem o nome do coordenador associado ao evento
    class Meta:
        model = Eventos
        fields = ['nome_evento', 'descricao', 'data_inicio', 'data_fim', 'local', 'coordenador', 'ativo', 'logo']
        read_only_fields = ('id', 'created_at', 'updated_at') # 

    def create(self, validated_data):
        coordenador = self.context['coordenador'] # Obtém o coordenador do contexto que foi passado na view
        return Eventos.objects.create(coordenador=coordenador, **validated_data) # Cria um novo evento com os dados validados e o coordenador associado


    # Obtém o nome do coordenador associado ao evento
    def get_coordenador(self, obj): # obj é a instância do modelo Eventos
        return obj.coordenador.nome if obj.coordenador and obj.coordenador.nome else 'Coordenador não definido'


    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    

    def partial_update(self, instance, validated_data):
        return super().partial_update(instance, validated_data)


class DesativarEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eventos
        fields = ['ativo']
        read_only_fields = ('id', 'created_at', 'updated_at')

    def update(self, instance, validated_data):
        instance.ativo = False  # Define o campo ativo como False
        instance.save()  # Salva a instância atualizada
        return instance  # Retorna a instância atualizada