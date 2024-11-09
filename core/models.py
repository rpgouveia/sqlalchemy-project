from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class Client(Base):
    __tablename__           = "client"
    name: Mapped[str]       = mapped_column(String(255), nullable=False)
    cpf: Mapped[str]        = mapped_column(String(11), nullable=False, unique=True)
    birthdate: Mapped[date] = mapped_column(Date, nullable=False)
    address_1: Mapped[str]  = mapped_column(String(255), nullable=False)
    address_2: Mapped[str]  = mapped_column(String(255), nullable=True)
    post_code: Mapped[str]  = mapped_column(String(8), nullable=False)
    city: Mapped[str]       = mapped_column(String(255), nullable=False)
    state: Mapped[str]      = mapped_column(String(2), nullable=False)
    country: Mapped[str]    = mapped_column(String(2), nullable=False)
    phone: Mapped[str]      = mapped_column(String(11), nullable=False)
    email: Mapped[str]      = mapped_column(String(255), nullable=False, unique=True)

    @property
    def age(self) -> int:
        today: date = date.today()
        age: int = today.year - self.birthdate.year
        if today < self.birthdate.replace(year=today.year):
            age -= 1
        return age

    def __repr__(self) -> str:
        return (
            f"Client(\n"
            f"  id: {self.id},\n"
            f"  name: {self.name},\n"
            f"  cpf: {self.cpf},\n"
            f"  birthdate: {self.birthdate},\n"
            f"  age: {self.age},\n"
            f"  address_1: {self.address_1},\n"
            f"  address_2: {self.address_2},\n"
            f"  post_code: {self.post_code},\n"
            f"  city: {self.city},\n"
            f"  state: {self.state},\n"
            f"  country: {self.country},\n"
            f"  phone: {self.phone},\n"
            f"  email: {self.email}\n"
            f")"
        )


class Users(Base):
    __tablename__           = "users"
    username: Mapped[str]     = mapped_column(String(255), nullable=False, unique=True)
    fullname: Mapped[str]     = mapped_column(String(255), nullable=False)
    phone: Mapped[str]        = mapped_column(String(11), nullable=False, unique=True)
    email: Mapped[str]        = mapped_column(String(255), nullable=False, unique=True)
    access_level: Mapped[str] = mapped_column(String(20), nullable=False)

    def __repr__(self) -> str:
        return (
            f"User(\n"
            f"  id: {self.id},\n"
            f"  username: {self.username},\n"
            f"  fullname: {self.fullname},\n"
            f"  phone: {self.phone},\n"
            f"  email: {self.email}\n"
            f"  access_level: {self.access_level}\n"
            f")"
        )
