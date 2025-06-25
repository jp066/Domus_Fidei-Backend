# Guia de Validação de Token JWT

## Como verificar se o token expirou no seu projeto Django

Seu projeto usa **SimpleJWT** para autenticação. Existem várias formas de verificar se um token expirou:

## 1. Verificação Automática (Recomendada)

O Django REST Framework com SimpleJWT **já faz a verificação automaticamente** quando você usa:

```python
from rest_framework.permissions import IsAuthenticated

class MinhaView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def minha_action(self, request):
        # Se chegou até aqui, o token é válido e não expirou
        # O Django já rejeitou tokens expirados automaticamente
        pass
```

## 2. Verificação Manual (Se necessário)

Caso precise fazer verificação manual do token:

```python
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.response import Response
from rest_framework import status

def verificar_token_manualmente(self, request):
    try:
        # Obtém o token do cabeçalho Authorization
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response(
                {'error': 'Token não encontrado'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        token_str = auth_header.split(' ')[1]
        
        # Verifica se o token é válido (incluindo expiração)
        token = AccessToken(token_str)
        
        # Se chegou até aqui, o token é válido
        return True
        
    except TokenError as e:
        return Response(
            {'error': f'Token inválido ou expirado: {str(e)}'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
```

## 3. Verificação usando request.auth

```python
def verificar_com_request_auth(self, request):
    # request.auth contém o token decodificado (se válido)
    if not request.auth:
        return Response(
            {'error': 'Token não encontrado ou inválido'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # O token é válido se request.auth não for None
    user_id = request.auth.get('user_id')
    return user_id
```

## 4. Tratamento de Exceções Específicas

```python
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

try:
    token = AccessToken(token_string)
    # Token válido
except TokenError:
    # Token expirado ou inválido
    pass
except InvalidToken:
    # Token malformado
    pass
```

## Configurações de Expiração no settings.py

Suas configurações atuais:

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # Token expira em 1 hora
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),     # Refresh token expira em 1 dia
    'ROTATE_REFRESH_TOKENS': True,
    # ... outras configurações
}
```

## Códigos de Erro Comuns

- **401 Unauthorized**: Token expirado, inválido ou não fornecido
- **403 Forbidden**: Token válido mas usuário sem permissão

## Dica Importante

**Não** é necessário verificar manualmente a expiração do token na maioria dos casos. O Django REST Framework já faz isso automaticamente quando você usa `IsAuthenticated` ou outras permissões de autenticação.

A verificação manual só é necessária em casos específicos onde você precisa de controle mais granular sobre o processo de autenticação.
