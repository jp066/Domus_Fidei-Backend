from rest_framework import serializers
from .models import (
    RetiroAcampamento, EquipeRetiro, 
    ServoRetiro, CronogramaRetiro, 
    InscricaoRetiro, Eventos,
    Formacoes, AssembleiaParoquial
)
from .models import (
    Eventos, AssembleiaParoquial
)
from rest_framework.exceptions import ValidationError


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
    

class AssembleiaParoquialSerializer(serializers.ModelSerializer):
    paroco = serializers.SerializerMethodField()
    class Meta:
        model = AssembleiaParoquial
        fields = ['id', 'paroco', 'tema_assembleia', 'data_assembleia', 'local']
        read_only_fields = ['id']

    def get_paroco_responsavel(self, obj):
        return obj.pessoa.nome if obj.paroco and obj.paroco.pessoa else 'Pároco não definido'
    
    def validate(self, attrs):
        if not attrs.get('tema_assembleia'):
            raise ValidationError("O campo 'tema_assembleia' é obrigatório.")
        if not attrs.get('data_assembleia'):
            raise ValidationError("O campo 'data_assembleia' é obrigatório.")
        if not attrs.get('local'):
            raise ValidationError("O campo 'local' é obrigatório.")
        return attrs


    def create(self, validated_data):
        paroco = self.context.get('paroco')
        validated_data['paroco'] = paroco
        return AssembleiaParoquial.objects.create(**validated_data)
    # estava fazendo isso, além de conferindo um erro.


    def list(self, instance):
        paroco = self.context.get('paroco')
        serializer = AssembleiaParoquialSerializer(instance, many=True, context={'paroco': paroco})
        return serializer.data