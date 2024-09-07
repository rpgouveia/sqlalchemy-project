from sqlalchemy import String, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date
import re


class Base(DeclarativeBase):
    pass


# Client Table
class Client(Base):
    __tablename__                 = "client"
    id: Mapped[int]               = mapped_column(primary_key=True)
    name: Mapped[str]             = mapped_column(String(100), nullable=False)
    cpf: Mapped[str]              = mapped_column(String(11), nullable=False)
    birthdate: Mapped[date]       = mapped_column(Date, nullable=False)
    address: Mapped[str]          = mapped_column(String(255), nullable=True)
    phone: Mapped[str]            = mapped_column(String(11), nullable=False)
    email: Mapped[str]            = mapped_column(String(255), nullable=False, unique=True)

    # Birthdate Default Format: YYYY-MM-DD
    # CPF Validation, only numbers
    @property
    def cpf(self) -> str:
        if not self.__cpf or not re.match(r"^\d{11}$", self.__cpf):
            raise ValueError("CPF inválido. Deve conter 11 dígitos numéricos.")
        return self.__cpf

    @cpf.setter
    def cpf(self, value: str):
        self.__cpf = value


    # Phone Number Validation, only numbers
    @property
    def phone(self) -> str:
        if not self.__phone or not re.match(r"^\d{11}$", self.__phone):
            raise ValueError("Telefone inválido. Deve conter 11 dígitos numéricos.")
        return self.__phone

    @phone.setter
    def phone(self, value: str):
        self.__phone = value

    @property
    def age(self) -> int:
        today: date = date.today()
        age: int = today.year - self.birthdate.year
        return age

    def __repr__(self) -> str:
        return (
            f"Client(\n"
            f"  id: {self.id},\n"
            f"  name: {self.name},\n"
            f"  cpf: {self.cpf},\n"
            f"  birthdate: {self.birthdate},\n"
            f"  age: {self.age},\n"
            f"  address: {self.address},\n"
            f"  phone: {self.phone},\n"
            f"  email: {self.email}\n"
            f")"
        )

