import re
from datetime import date
from django.core.exceptions import ValidationError

def clean_digits(value):
    if not value:
        return ""
    return re.sub(r'\D', '', str(value))

def validar_data_nascimento(data_nascimento):
    if not data_nascimento:
        return data_nascimento

    if data_nascimento > date.today():
        raise ValidationError("A data de nascimento não pode ser no futuro.")
    
    return data_nascimento

def validar_cpf(cpf):
    cpf = clean_digits(cpf)
    
    if len(cpf) != 11:
        raise ValidationError("O CPF deve conter exatamente 11 dígitos.")
    
    if cpf == cpf[0] * 11:
        raise ValidationError("CPF inválido.")

    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = soma % 11
    if resto < 2:
        digito1 = 0
    else:
        digito1 = 11 - resto
    
    if int(cpf[9]) != digito1:
        raise ValidationError("CPF inválido.")

    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = soma % 11
    if resto < 2:
        digito2 = 0
    else:
        digito2 = 11 - resto
    
    if int(cpf[10]) != digito2:
        raise ValidationError("CPF inválido.")
    
    return cpf

def validar_telefone(telefone):
    telefone = clean_digits(telefone)
    
    if len(telefone) != 11:
        raise ValidationError("O telefone deve conter exatamente 11 dígitos (DDD + 9 números).")
    
    return telefone

def validar_cep(cep):
    cep = clean_digits(cep)
    
    if len(cep) != 8:
        raise ValidationError("O CEP deve conter exatamente 8 dígitos.")
    
    return cep
