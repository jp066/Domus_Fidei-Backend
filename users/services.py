from django.db import transaction 
# o decorator @transaction.atomic é usado para garantir que todas as operações dentro do bloco sejam tratadas como uma única transação. 
# Se qualquer operação falhar, todas as alterações serão revertidas, garantindo a integridade dos dados.
from .models import Pessoa, Paroco, PerfilPessoa
# seria a mesma coisa que criar um método create na classe PessoaSerializer, 
# mas aqui estou criando uma função separada para encapsular a lógica de criação de uma pessoa com perfil de paroco e ao mesmo tempo criando um Paroco.
# assim, o transaction.atomic garante que tanto a criação da Pessoa quanto a do Paroco sejam feitas de forma atômica, 
# ou seja, ambas serão salvas ou nenhuma será salva em caso de erro.

def criar_pessoa_com_perfil(validated_data):
    with transaction.atomic():
        password = validated_data.pop('password')
        pessoa = Pessoa(**validated_data)
        pessoa.set_password(password)
        pessoa.save()
        if pessoa.perfil_pessoa == PerfilPessoa.PAROCO:
            identificador_paroco = f"PADRE_{pessoa.codigo_acesso}"
            Paroco.objects.create(pessoa=pessoa, identificador_paroco=identificador_paroco)

        return pessoa