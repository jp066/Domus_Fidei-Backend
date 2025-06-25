from django.shortcuts import render
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import CriarSacramentoSerializer
from .models import Sacramento
from users.permissions import PerfilPermitido
