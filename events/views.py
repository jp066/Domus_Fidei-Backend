from rest_framework import viewsets, status
from .models import Eventos
from rest_framework.response import Response
from users.permissions import PerfilPermitido
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .serializers import (
    EventosSerializer, DesativarEventoSerializer
    )
from rest_framework.parsers import JSONParser, FormParser

class EventosViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.action == 'criar_evento':
            return [PerfilPermitido('COORD_MINISTERIO')]
        
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['post'], url_path='criar')
    def criar_evento(self, request):
        parser_classes = [JSONParser, FormParser]  # Permite o envio de arquivos e dados JSON
        coordenador = request.user  # Obtém o coordenador associado ao usuário autenticado
        serializer = EventosSerializer(data=request.data, context={'coordenador': coordenador}) # request.data é o dicionário de dados enviados na requisição, ou seja, todos os dados do serializer
        if serializer.is_valid(): # verifica se os dados são válidos
            evento = serializer.save() # salva o evento com o usuário logado como coordenador
            return Response({
                'message': 'Evento criado com sucesso!',
                'data': {
                    'id': evento.id,
                    'nome_evento': evento.nome_evento,
                    'coordenador': coordenador.nome,  # ou coordenador.pessoa.nome se quiser o nome completo
                    'data_inicio': evento.data_inicio,
                    'data_fim': evento.data_fim,
                    'local': evento.local
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @action(detail=True, methods=['patch'], url_path='atualizar')
    def atualizar_evento(self, request, pk=None):
        try:
            evento = Eventos.objects.get(pk=pk)  # Obtém o evento com base no pk fornecido
            serializer = EventosSerializer(evento, data=request.data, partial=True)  # partial=True permite atualizar apenas alguns campos
            serializer.is_valid(raise_exception=True)  # Valida os dados do serializer
            evento_atualizado = serializer.save()
            return Response({
                'message': 'Evento atualizado com sucesso!',
                'data': {
                    'id': evento_atualizado.id,
                    'nome_evento': evento_atualizado.nome_evento,
                    'data_inicio': evento_atualizado.data_inicio,
                    'data_fim': evento_atualizado.data_fim,
                    'local': evento_atualizado.local,
                    'coordenador': evento_atualizado.coordenador,
                    'ativo': evento_atualizado.ativo,
                    'logo': evento_atualizado.logo
                }
            }, status=status.HTTP_200_OK)
        except Eventos.DoesNotExist:
            return Response({'error': 'Evento não encontrado'}, status=status.HTTP_404_NOT_FOUND)


    @action(detail=True, methods=['post'], url_path='desativar')
    def desativar_evento(self, request, pk=None):
        try:
            evento = Eventos.objects.get(pk=pk)  # Obtém o evento com base no pk fornecido
            serializer = DesativarEventoSerializer(evento, data=request.data, partial=True)  # partial=True permite atualizar apenas alguns campos
            serializer.is_valid(raise_exception=True)  # Valida os dados do serializer
            evento_atualizado = serializer.save()
            return Response({
                'message': 'Evento desativado com sucesso!',
                'data': {
                    'id': evento_atualizado.id,
                    'nome_evento': evento_atualizado.nome_evento,
                    'ativo': evento_atualizado.ativo
                }
            }, status=status.HTTP_200_OK)
        except Eventos.DoesNotExist:
            return Response({'error': 'Evento não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        

    def list(self, request):
        eventos = Eventos.objects.all()
        serializer = EventosSerializer(eventos, many=True) # many=True indica que estamos serializando múltiplos objetos
        return Response({
            'message': 'Lista de eventos',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        try:
            evento = Eventos.objects.get(pk=pk)
            serializer = EventosSerializer(evento)
            return Response({
                'message': 'Evento encontrado',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Eventos.DoesNotExist:
            return Response({'error': 'Evento não encontrado'}, status=status.HTTP_404_NOT_FOUND)