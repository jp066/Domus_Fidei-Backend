from rest_framework import serializers
from .models import SacramentoParoquial, AgendamentoSacramento as Agendamento
from users.serializers import PessoaSerializer
from users.permissions import PerfilPermitido
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError


# esse serializer é usado para serializar os dados do SacramentoParoquial
class SacramentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SacramentoParoquial
        fields = ['id', 'paroco_responsavel', 'nome_sacramento']
        read_only_fields = ['id', 'paroco_responsavel']

    def validate(self, attrs):
        if not attrs.get('paroco_responsavel'):
            raise ValidationError("O campo 'paroco_responsavel' é obrigatório.")
        if not attrs.get('nome_sacramento'):
            raise ValidationError("O campo 'nome_sacramento' é obrigatório.")
        return attrs


# já esse serializer é usado para criar um novo SacramentoParoquial
class CriarSacramentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SacramentoParoquial
        fields = ['nome_sacramento']
    

    def create(self, validated_data):
    pessoa = self.context['pessoa']
    return Agendamento.objects.create(pessoa=pessoa, **validated_data)


class AgendamentoSacramentoSerializer(serializers.ModelSerializer):
    sacramento = serializers.PrimaryKeyRelatedField(queryset=SacramentoParoquial.objects.all())
    pessoa = serializers.PrimaryKeyRelatedField(queryset=None, read_only=True)  # Will be set in view
    
    class Meta:
        model = Agendamento
        fields = ['id', 'sacramento', 'pessoa', 'data_solicitada', 'aprovado']
        read_only_fields = ['id', 'pessoa', 'aprovado']

    def validate(self, attrs):
        if not attrs.get('sacramento'):
            raise ValidationError("O campo 'sacramento' é obrigatório.")
        if not attrs.get('data_solicitada'):
            raise ValidationError("O campo 'data_solicitada' é obrigatório.")
        return attrs
    
    def create(self, validated_data):
        # A pessoa será definida na view
        agendamento = Agendamento.objects.create(**validated_data)
        return agendamento


class AgendamentoSacramentoReadSerializer(serializers.ModelSerializer):
    """Serializer for reading agendamentos with detailed information"""
    sacramento = SacramentoSerializer(read_only=True)
    pessoa = PessoaSerializer(read_only=True)
    
    class Meta:
        model = Agendamento
        fields = ['id', 'sacramento', 'pessoa', 'data_agendamento', 'data_solicitada', 'aprovado']
        read_only_fields = ['id', 'data_agendamento']
