from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import (
    SacramentoSerializer,
    CriarSacramentoSerializer,
    AgendamentoSacramentoSerializer, 
    AgendamentoSacramentoReadSerializer)
from .models import SacramentoParoquial as Sacramento, AgendamentoSacramento as Agendamento
from users.permissions import PerfilPermitido


class SacramentoViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.action == 'criar_sacramento': # Verifica se a ação é 'criar_sacramento'
            return [PerfilPermitido('PAROCO')] # Permite apenas usuários com perfil de 'PAROCO'
        #if self.action in ['list', 'retrieve', 'destroy']: # Verifica se a ação é 'list', 'retrieve' ou 'destroy'
        #    return [PerfilPermitido('PAROCO')]
        return [IsAuthenticated()] # Permite apenas usuários autenticados para outras ações

    
    def list(self, request):
        paroco = request.user  # Obtém o pároco associado ao usuário autenticado
        sacramentos = Sacramento.objects.all()
        serializer = SacramentoSerializer(sacramentos, many=True, context={'paroco': paroco})  # Passa o pároco no contexto para o serializer
        return Response({
            'message': 'Lista de sacramentos:',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    

    def retrieve(self, request, pk=None):
        try:
            sacramento = Sacramento.objects.get(pk=pk)
            serializer = CriarSacramentoSerializer(sacramento)
            return Response({
                'message': 'Detalhes do sacramento:',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Sacramento.DoesNotExist:
            return Response({'error': 'Sacramento não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    

    @action(detail=False, methods=['post'], url_path='criar') # url_path define o endpoint
    def criar_sacramento(self, request):
        paroco = request.user.paroco  # Obtém o pároco associado ao usuário autenticado
        serializer_class = CriarSacramentoSerializer(data=request.data, context={'paroco': paroco})
        if serializer_class.is_valid():
            # Define o pároco responsável automaticamente
            sacramento = serializer_class.save()
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
        pessoa = request.user  # Obtém a pessoa associada ao usuário autenticado
        serializer = AgendamentoSacramentoSerializer(
            data=request.data, 
            context={'pessoa': pessoa}
            ) # Cria um serializer com os dados da requisição e o contexto da pessoa autenticada
        if serializer.is_valid():
            agendamento = serializer.save()
            read_serializer = AgendamentoSacramentoReadSerializer(agendamento, context={'pessoa':pessoa}) # Serializa o agendamento criado
            
            return Response({
                'message': 'Agendamento criado com sucesso!',
                'data': read_serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # Retorna erros de validação se houverem
    
    
    @action(detail=False, methods=['get'], url_path='meus-agendamentos')
    def listar_agendamentos(self, request):
        pessoa = request.user
        agendamentos = Agendamento.objects.filter(pessoa=pessoa)
        serializer = AgendamentoSacramentoReadSerializer(agendamentos, many=True) # Serializa todos os agendamentos da pessoa
        
        return Response({
            'message': 'Agendamentos listados:',
            'data': serializer.data
        }, status=status.HTTP_200_OK) # Retorna a lista de agendamentos da pessoa autenticada
    

    @action(detail=True, methods=['delete'], url_path='excluir-agendamento')
    def apagar_agendamento(self, request, pk=None):
        serializer = AgendamentoSacramentoSerializer()  # Cria uma instância do serializer para usar o método de deleção
        try:
            agendamento = Agendamento.objects.get(pk=pk)  # Obtém o agendamento com base no pk fornecido
            serializer.destroy(agendamento)  # Chama o método de deleção do serializer
            return Response({'message': 'Agendamento deletado com sucesso!'}, status=status.HTTP_204_NO_CONTENT)
        except Agendamento.DoesNotExist:
            return Response({'error': 'Agendamento não encontrado'}, status=status.HTTP_404_NOT_FOUND)