from rest_framework import serializers
from .models import Pessoa, Paroco, PerfilPessoa
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated


class PessoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pessoa
        fields = ['id', 'codigo_acesso', 'nome','email', 'comunidade', 'perfil_pessoa', 'password']
        read_only_fields = ['codigo_acesso']

    def create(self, validated_data):
        # Preenche o campo username com o mesmo valor de codigo_acesso
        validated_data['username'] = validated_data.get('codigo_acesso')
        password = validated_data.pop('password')
        pessoa = Pessoa(**validated_data)
        pessoa.set_password(password)
        pessoa.save()        
        return pessoa


    def update(self, instance, validated_data):
        return super().update(instance, validated_data)    


class ParocoSerializer(serializers.ModelSerializer):
    pessoa = PessoaSerializer()

    class Meta:
        model = Paroco
        fields = ['pessoa', 'identificador_paroco']
        read_only_fields = ['pessoa']
            

    def update(self, instance, validated_data):
        pessoa_data = validated_data.pop('pessoa', None)
        if pessoa_data:
            for attr, value in pessoa_data.items():
                setattr(instance.pessoa, attr, value)
            instance.pessoa.save()
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance