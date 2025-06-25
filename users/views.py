from django.http import HttpResponse
from .models import Pessoa, Paroco
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import PessoaSerializer, ParocoSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import PerfilPermitido

class PessoaViewSet(viewsets.ViewSet):

    def get_permissions(self):
        if self.action in ['meu_perfil']:
            return [IsAuthenticated()] # 
        
        return [IsAuthenticated]

    def create(self, request):
        serializer = PessoaSerializer(data=request.data)
        if serializer.is_valid():
            pessoa = serializer.save()
            return Response({'message': 'Usuário criado com sucesso!', 'data': PessoaSerializer(pessoa).data}, status=201)
        return Response(serializer.errors, status=400)
    # essa view cadastra uma pessoa.
    

    @action(detail=False, methods=['get'], url_path='meu-perfil')
    def meu_perfil(self, request):
        pessoa = request.user.nome
        serializer = PessoaSerializer(request.user)
        return Response(serializer.data)


    @action(detail=False, methods=['post'], url_path='criar-paroco')
    def criar_paroco(self, request):
        serializer = ParocoSerializer()
        try:
            paroco = serializer.add_paroco(request.data)
            return Response({
                'message': 'Pároco criado com sucesso!',
                'data': {
                    'pessoa': PessoaSerializer(paroco.pessoa).data,
                    'identificador_paroco': paroco.identificador_paroco
                }
            }, status=201)
        except serializers.ValidationError as e:
            return Response({'errors': e.detail}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
    # essa view cadastra um padre.
