
def validar_dados_carro(data, arquivos=None):
    erros = []

    campos_obrigatorios = [
        'brand', 'car_model', 'mileage', 'year', 'fuel_type',
        'type', 'price', 'color', 'description'
    ]

    for campo in campos_obrigatorios:
        if not data.get(campo):
            erros.append(f'O campo {campo} é obrigatório.')

    try:
        if data.get('year') and (int(data.get('year')) < 1900 or int(data.get('year')) > 2100):
            erros.append('Ano inválido.')
    except ValueError:
        erros.append('Ano deve ser um número.')

    try:
        if data.get('mileage') and int(data.get('mileage')) < 0:
            erros.append('Quilometragem deve ser um número positivo.')
    except ValueError:
        erros.append('Quilometragem deve ser um número.')

    try:
        if data.get('price') and float(data.get('price')) < 0:
            erros.append('Preço deve ser um valor positivo.')
    except ValueError:
        erros.append('Preço deve ser um número válido.')

    if arquivos:
        if not arquivos.get('image'):
            erros.append('A imagem é obrigatória.')

    return erros
