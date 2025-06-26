from django.http import HttpResponse
from .models import Pessoa, Paroco
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import PessoaSerializer, ParocoSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import PerfilPermitido
from functools import wraps
from typing import Dict, Any, List, Optional


def validate_data_complete(required_fields: List[str], unique_fields: Optional[List[str]] = None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if len(args) < 2:
                return func(*args, **kwargs)
            
            request = args[1]
            
            # Verifica se o usuário já está autenticado
            if hasattr(request, 'user') and request.user and request.user.is_authenticated:
                return Response(
                    {'error': 'Usuário já autenticado'}, 
                    status=400
                )
            
            for field in required_fields:
                if not request.data.get(field):
                    return Response(
                        {'error': f'{field.capitalize()} é obrigatório'}, 
                        status=400
                    )
            
            # Validar campos únicos
            if unique_fields:
                for field in unique_fields:
                    value = request.data.get(field)
                    if value:
                        if field == 'email' and Pessoa.objects.filter(email=value).exists():
                            return Response(
                                {'error': 'Email já cadastrado'}, 
                                status=400
                            )
                        # Adicione outras validações de unicidade aqui se necessário
            
            return func(*args, **kwargs)
        return wrapper
    return decorator