from django.shortcuts import render
from rest_framework import viewsets, serializers, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import CriarSacramentoSerializer, AgendamentoSacramentoSerializer, AgendamentoSacramentoReadSerializer
from .models import SacramentoParoquial as Sacramento, AgendamentoSacramento as Agendamento
from users.permissions import PerfilPermitido


class SacramentoViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.action == 'criar_sacramento': # Verifica se a ação é 'criar_sacramento'
            return [PerfilPermitido('PAROCO')] # Permite apenas usuários com perfil de 'PAROCO'

        return [IsAuthenticated()] # Permite apenas usuários autenticados para outras ações
    

    @action(detail=False, methods=['post'], url_path='criar') # url_path define o endpoint
    def criar_sacramento(self, request):
        try:
            paroco = request.user.paroco # Busca o pároco baseado no usuário logado
        except AttributeError:
            return Response(
                {'error': 'Usuário logado não é um pároco'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer_class = CriarSacramentoSerializer(data=request.data)
        if serializer_class.is_valid():
            # Define o pároco responsável automaticamente
            sacramento = serializer_class.save(paroco_responsavel=paroco)
            return Response({
                'message': 'Sacramento criado com sucesso!',
                'data': {
                    'id': sacramento.id,
                    'nome_sacramento': sacramento.nome_sacramento,
                    'paroco_responsavel': paroco.pessoa.nome
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)


class AgendamentoViewSet(viewsets.ViewSet):

    def get_permissions(self):
        if self.action == 'criar_agendamento': # Verifica se a ação é 'criar_agendamento'
            return [IsAuthenticated()]
    
        return [IsAuthenticated()] # Permite apenas usuários autenticados para outras ações
    
    @action(detail=False, methods=['post'], url_path='agendar')
    def criar_agendamento(self, request):
        # Verifica se o usuário está autenticado
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Usuário não está autenticado'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        # Verifica se o usuário tem uma pessoa associada
        # Como Pessoa é o modelo de usuário customizado, request.user já é uma instância de Pessoa
        pessoa = request.user
        if not pessoa:
            return Response(
                {'error': 'Usuário logado não possui uma pessoa associada'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        serializer = AgendamentoSacramentoSerializer(data=request.data, context={'pessoa': pessoa})
        if serializer.is_valid():
            agendamento = serializer.save(pessoa=pessoa)
            read_serializer = AgendamentoSacramentoReadSerializer(agendamento) # Serializa o agendamento criado
            
            return Response({
                'message': 'Agendamento criado com sucesso!',
                'data': read_serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # Retorna erros de validação se houverem
    
    
    @action(detail=False, methods=['get'], url_path='meus-agendamentos')
    def listar_agendamentos(self, request):


        pessoa = request.user # usuario autenticado
        agendamentos = Agendamento.objects.filter(pessoa=pessoa)
        serializer = AgendamentoSacramentoReadSerializer(agendamentos, many=True) # Serializa todos os agendamentos da pessoa
        
        return Response({
            'message': 'Agendamentos listados:',
            'data': serializer.data
        }, status=status.HTTP_200_OK) # Retorna a lista de agendamentos da pessoa autenticada
