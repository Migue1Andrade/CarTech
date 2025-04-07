from django.contrib.auth.models import User

def validar_dados_usuario(data):
    erros = []

    username = data.get('username')
    senha1 = data.get('password1')
    senha2 = data.get('password2')

    if not username:
        erros.append('Nome de usuário é obrigatório.')
    elif User.objects.filter(username=username).exists():
        erros.append('Esse nome de usuário já está em uso.')

    if not senha1 or not senha2:
        erros.append('Os dois campos de senha são obrigatórios.')
    elif senha1 != senha2:
        erros.append('As senhas não coincidem.')
    elif len(senha1) < 6:
        erros.append('A senha deve ter pelo menos 6 caracteres.')

    return erros
