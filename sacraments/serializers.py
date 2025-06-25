from rest_framework import serializers
from .models import Sacramento
from users.serializers import PessoaSerializer
from users.permissions import PerfilPermitido
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError


class SacramentoSerializer(serializers.ModelSerializer):
    pessoa = PessoaSerializer(read_only=True)

    class Meta:
        model = Sacramento
        fields = ['id', 'pessoa', 'tipo_sacramento', 'data', 'local', 'observacoes']
        read_only_fields = ['id', 'pessoa']

    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise ValidationError("Usuário não autenticado.")
        
        validated_data['pessoa'] = request.user.pessoa
        return super().create(validated_data)
