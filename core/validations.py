from datetime import date
import re


def validate_cpf(cpf: str) -> str:
    cleaned_cpf = re.sub(r'\D', '', cpf)
    if not re.match(r"^\d{11}$", cleaned_cpf):
        raise ValueError("CPF inválido. Deve conter 11 dígitos numéricos.")
    return cleaned_cpf

def validate_phone(phone: str) -> str:
    cleaned_phone = re.sub(r'\D', '', phone)
    if not re.match(r"^\d{10,11}$", cleaned_phone):
        raise ValueError("Telefone inválido. Deve conter 10 ou 11 dígitos numéricos.")
    return cleaned_phone

def validate_birthdate(birthdate_str: str) -> date:
    try:
        birthdate = date.fromisoformat(birthdate_str)
        return birthdate
    except ValueError:
        raise ValueError("Data de nascimento inválida. O formato deve ser AAAA-MM-DD.")

def validate_option(prompt) -> int:
    while True:
        try:
            option = int(input(prompt))
            return option
        except ValueError:
            print("Opção inválida. Por favor, digite um número inteiro.")

