from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date


class Base(DeclarativeBase):
    pass


# Client Table
class Client(Base):
    __tablename__                 = "client"
    id: Mapped[int]               = mapped_column(primary_key=True)
    name: Mapped[str]             = mapped_column(String(100), nullable=False)
    cpf: Mapped[int]              = mapped_column(Integer(), nullable=False)
    birthdate: Mapped[date]       = mapped_column(Date, nullable=False)           # Default Format YYYY-MM-DD
    address: Mapped[str]          = mapped_column(String(255), nullable=True)
    phone: Mapped[int]            = mapped_column(Integer(), nullable=False)
    email: Mapped[str]            = mapped_column(String(255), nullable=False, unique=True)

    # CPF Validation >> 11 numbers limit, no mask >> 123.456.789-10
    

    # Phone Number Validation >> 11 numbers limit, no mask >> (12) 98765-4321

    # Decorator
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

