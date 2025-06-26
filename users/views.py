from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import PessoaSerializer
from .decorators import validate_data_complete
from .services import criar_pessoa_com_perfil


class PessoaViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.action in ['meu_perfil']:
            return [IsAuthenticated()] # 
        return [AllowAny()]  # Permite acesso a qualquer usuário para criar um novo perfil
    

    @validate_data_complete(['email', 'password', 'nome'], ['email'])
    def create(self, request):
        serializer_class = PessoaSerializer(data=request.data)
        if serializer_class.is_valid():
            pessoa = criar_pessoa_com_perfil(serializer_class.validated_data)
            return Response({'message': 'Usuário criado com sucesso!', 'data': PessoaSerializer(pessoa).data}, status=201)
        return Response(serializer_class.errors, status=400)
    

    @action(detail=False, methods=['get'], url_path='meu-perfil')
    def meu_perfil(self, request):
        pessoa = request.user.nome
        serializer = PessoaSerializer(request.user)
        return Response(serializer.data)