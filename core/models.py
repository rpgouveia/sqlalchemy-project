from sqlalchemy import Integer, Numeric, String, Date, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import date


class Base(DeclarativeBase):
    pass


# Accidents Table
class Accidents(Base):
    __tablename__                   = "accidents"
    id: Mapped[int]                 = mapped_column(primary_key=True)
    accident_date: Mapped[date]     = mapped_column(Date, nullable=False)
    description: Mapped[str]        = mapped_column(String(255), nullable=False)
    repair_cost: Mapped[Numeric]    = mapped_column(Numeric(precision=10, scale=2, asdecimal=True), nullable=False)
    insurance_id: Mapped[int]       = mapped_column(ForeignKey("insurance.id"))
    apartment_id: Mapped[int]       = mapped_column(ForeignKey("apartment.id"))

    def __repr__(self) -> str:
        return (
            f"Accidents(\n"
            f"  id: {self.id},\n"
            f"  accident_date: {self.accident_date},\n"
            f"  description: {self.description},\n"
            f"  repair_cost: {self.repair_cost},\n"
            f"  insurance_id: {self.insurance_id}\n"
            f"  apartment_id: {self.apartment_id}\n"
            f")"
        )


# Insurance Table
class Insurance(Base):
    __tablename__                   = "insurance"
    id: Mapped[int]                 = mapped_column(primary_key=True)
    # insurance_number: Mapped[int]   = mapped_column(Integer(11), nullable=False, unique=True) # Problema no SQLite
    insurance_number: Mapped[int]   = mapped_column(Integer(), nullable=False, unique=True)
    start_date: Mapped[date]        = mapped_column(Date, nullable=False)
    end_date: Mapped[date]          = mapped_column(Date, nullable=True)
    insured_value: Mapped[Numeric]  = mapped_column(Numeric(precision=10, scale=2, asdecimal=True), nullable=False)
    prize: Mapped[Numeric]          = mapped_column(Numeric(precision=10, scale=2, asdecimal=True), nullable=False)
    client_id: Mapped[int]          = mapped_column(ForeignKey("client.id"), nullable=True)
    apartment_id: Mapped[int]       = mapped_column(ForeignKey("apartment.id"), nullable=True)

    def __repr__(self) -> str:
        return (
            f"Insurance(\n"
            f"  id: {self.id},\n"
            f"  insurance_number: {self.insurance_number},\n"
            f"  start_date: {self.start_date},\n"
            f"  end_date: {self.end_date},\n"
            f"  insured_value: {self.insured_value},\n"
            f"  prize: {self.prize},\n"
            f"  client_id: {self.client_id}\n"
            f"  apartment_id: {self.apartment_id}\n"
            f")"
        )


# Apartment Table
class Apartment(Base):
    __tablename__                   = "apartment"
    id: Mapped[int]                 = mapped_column(primary_key=True)
    # apartment_number: Mapped[int]   = mapped_column(Integer(4), nullable=False, unique=True)  # Problema no SQLite
    apartment_number: Mapped[int]   = mapped_column(Integer(), nullable=False, unique=True)
    address: Mapped[str]            = mapped_column(String(255), nullable=False)
    # area: Mapped[int]               = mapped_column(Integer(4), nullable=False)               # Problema no SQLite
    area: Mapped[int]               = mapped_column(Integer(), nullable=False)
    client_id: Mapped[int]          = mapped_column(ForeignKey("client.id"))
    insurance_id: Mapped[int]       = mapped_column(ForeignKey("insurance.id"))

    def __repr__(self) -> str:
        return (
            f"Apartment(\n"
            f"  id: {self.id},\n"
            f"  insurance_number: {self.insurance_number},\n"
            f"  address: {self.address},\n"
            f"  area: {self.area}\n"
            f"  client_id: {self.client_id}\n"
            f"  insurance_id: {self.insurance_id}\n"
            f")"
        )


# Client Table
class Client(Base):
    __tablename__                 = "client"
    id: Mapped[int]               = mapped_column(primary_key=True)
    name: Mapped[str]             = mapped_column(String(100), nullable=False)
    # cpf: Mapped[int]              = mapped_column(Integer(11), nullable=False)  # Problema no SQLite
    cpf: Mapped[int]              = mapped_column(Integer(), nullable=False)
    birthdate: Mapped[date]       = mapped_column(Date, nullable=False)           # Default Format YYYY-MM-DD
    address: Mapped[str]          = mapped_column(String(255), nullable=True)     # Opcional? Conversar com professor
    # phone: Mapped[int]            = mapped_column(Integer(11), nullable=False)  # Problema no SQLite
    phone: Mapped[int]            = mapped_column(Integer(), nullable=False)
    email: Mapped[str]            = mapped_column(String(255), nullable=False, unique=True)
    insurances: Mapped[Insurance] = relationship("Insurance", backref="client")
    apartment: Mapped[Apartment]  = relationship("Apartment", backref="client")

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

