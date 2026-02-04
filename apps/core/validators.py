import re
from django.core.exceptions import ValidationError

def validate_cnpj(value):
    """
    Valida um número de CNPJ seguindo o algoritmo de dígitos verificadores.
    """
    # Remove caracteres não numéricos
    cnpj = re.sub(r'[^0-9]', '', str(value))

    # Verifica se tem 14 dígitos
    if len(cnpj) != 14:
        raise ValidationError("O CNPJ deve conter exatamente 14 números.")

    # Verifica se não é uma sequência de números repetidos (ex: 11.111.111/1111-11)
    if cnpj == cnpj[0] * 14:
        raise ValidationError("CNPJ inválido (números repetidos).")

    # Algoritmo de validação
    def calculate_digit(cnpj, weights):
        sum_val = sum(int(cnpj[i]) * weights[i] for i in range(len(weights)))
        remainder = sum_val % 11
        return '0' if remainder < 2 else str(11 - remainder)

    # Pesos para o primeiro dígito
    weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    # Pesos para o segundo dígito
    weights2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    # Valida primeiro dígito
    if cnpj[12] != calculate_digit(cnpj[:12], weights1):
        raise ValidationError("CNPJ inválido (dígito verificador incorreto).")

    # Valida segundo dígito
    if cnpj[13] != calculate_digit(cnpj[:13], weights2):
        raise ValidationError("CNPJ inválido (dígito verificador incorreto).")

    return cnpj
