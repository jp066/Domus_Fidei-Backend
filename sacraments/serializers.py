from rest_framework import serializers
from .models import SacramentoParoquial, AgendamentoSacramento as Agendamento
from users.serializers import PessoaSerializer
from users.permissions import PerfilPermitido
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

# esse serializer é usado para serializar os dados do SacramentoParoquial
class SacramentoSerializer(serializers.ModelSerializer):
    paroco_responsavel = serializers.SerializerMethodField()  # Obtém o nome do pároco responsável
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
    
    
    def get_paroco_responsavel(self, obj):
        return obj.paroco_responsavel.pessoa.nome if obj.paroco_responsavel and obj.paroco_responsavel.pessoa else 'Pároco não definido'
    

    def list(self, instance):
        paroco = self.context.get('paroco')  # Obtém o pároco do contexto
        serializer = SacramentoSerializer(instance, many=True, context={'paroco': paroco})
        return serializer.data


class CriarSacramentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SacramentoParoquial
        fields = ['nome_sacramento']

    def create(self, validated_data):
        paroco = self.context['paroco'] # Obtém o pároco do contexto que foi passado na view
        return SacramentoParoquial.objects.create(paroco_responsavel=paroco, **validated_data)


class AgendamentoSacramentoSerializer(serializers.ModelSerializer):
    sacramento = serializers.PrimaryKeyRelatedField(queryset=SacramentoParoquial.objects.all())

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
        pessoa = self.context.get('pessoa')
        validated_data['pessoa'] = pessoa
        agendamento = Agendamento.objects.create(**validated_data)
        return agendamento
    

    def destroy(self, instance):
        # Método para deletar um agendamento
        instance.delete()
        return instance


class AgendamentoSacramentoReadSerializer(serializers.ModelSerializer):
    """Serializer for reading agendamentos with detailed information"""
    sacramento = SacramentoSerializer(read_only=True)
    pessoa = serializers.SerializerMethodField()

    class Meta:
        model = Agendamento
        fields = ['id', 'sacramento', 'pessoa', 'data_agendamento', 'data_solicitada', 'aprovado']
        read_only_fields = ['id', 'data_agendamento']
    
    def get_pessoa(self, obj):
        """Returns the name of the person associated with the agendamento"""
        return obj.pessoa.nome if obj.pessoa else 'Pessoa não definida'