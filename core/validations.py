from datetime import date
import re


def validate_cpf(cpf: str) -> str:
    cleaned_cpf: str = re.sub(r'\D', '', cpf)
    if not re.match(r"^\d{11}$", cleaned_cpf):
        raise ValueError("CPF inválido. Deve conter 11 dígitos numéricos.")
    return cleaned_cpf


def validate_phone(phone: str) -> str:
    cleaned_phone: str = re.sub(r'\D', '', phone)
    if not re.match(r"^\d{10,11}$", cleaned_phone):
        raise ValueError("Telefone inválido. Deve conter 10 ou 11 dígitos numéricos.")
    return cleaned_phone


def validate_birthdate(birthdate_str: str) -> date:
    try:
        birthdate: date = date.fromisoformat(birthdate_str)
        return birthdate
    except ValueError:
        raise ValueError("Data de nascimento inválida. O formato deve ser AAAA-MM-DD.")


def validate_integer_number(prompt) -> int:
    while True:
        try:
            number: int = int(input(prompt))
            return number
        except ValueError:
            print("Opção inválida. Por favor, digite um número inteiro.")


def validate_email(email: str) -> str:
    email_pattern: str = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$"
    if not re.match(email_pattern, email):
        raise ValueError("Email inválido. Por favor, digite um email válido.")
    return email


def validate_post_code(post_code: str) -> str:
    cleaned_post_code: str = re.sub(r'\D', '', post_code)
    if not re.match(r"^\d{8}$", cleaned_post_code):
        raise ValueError("CEP inválido. Deve conter 8 dígitos numéricos.")
    return cleaned_post_code


def validate_state(state: str) -> str:
    if not re.match(r'^[A-Z]{2}$', state):
        raise ValueError("A sigla do estado deve conter exatamente 2 letras maiúsculas.")
    return state


def validate_country(country: str) -> str:
    if not re.match(r'^[A-Z]{2}$', country):
        raise ValueError("O código do país deve conter exatamente 2 letras maiúsculas.")
    return country

