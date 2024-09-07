# models.py

# Accidents Table
# class Accidents(Base):
#     __tablename__                   = "accidents"
#     id: Mapped[int]                 = mapped_column(primary_key=True)
#     accident_date: Mapped[date]     = mapped_column(Date, nullable=False)
#     description: Mapped[str]        = mapped_column(String(255), nullable=False)
#     repair_cost: Mapped[Numeric]    = mapped_column(Numeric(precision=10, scale=2, asdecimal=True), nullable=False)
#     insurance_id: Mapped[int]       = mapped_column(ForeignKey("insurance.id"))
#     apartment_id: Mapped[int]       = mapped_column(ForeignKey("apartment.id"))

#     def __repr__(self) -> str:
#         return (
#             f"Accidents(\n"
#             f"  id: {self.id},\n"
#             f"  accident_date: {self.accident_date},\n"
#             f"  description: {self.description},\n"
#             f"  repair_cost: {self.repair_cost},\n"
#             f"  insurance_id: {self.insurance_id}\n"
#             f"  apartment_id: {self.apartment_id}\n"
#             f")"
#         )


# Insurance Table
# class Insurance(Base):
#     __tablename__                   = "insurance"
#     id: Mapped[int]                 = mapped_column(primary_key=True)
#     insurance_number: Mapped[int]   = mapped_column(Integer(), nullable=False, unique=True)
#     start_date: Mapped[date]        = mapped_column(Date, nullable=False)
#     end_date: Mapped[date]          = mapped_column(Date, nullable=True)
#     insured_value: Mapped[Numeric]  = mapped_column(Numeric(precision=10, scale=2, asdecimal=True), nullable=False)
#     prize: Mapped[Numeric]          = mapped_column(Numeric(precision=10, scale=2, asdecimal=True), nullable=False)
#     client_id: Mapped[int]          = mapped_column(ForeignKey("client.id"), nullable=True)
#     apartment_id: Mapped[int]       = mapped_column(ForeignKey("apartment.id"), nullable=True)

#     def __repr__(self) -> str:
#         return (
#             f"Insurance(\n"
#             f"  id: {self.id},\n"
#             f"  insurance_number: {self.insurance_number},\n"
#             f"  start_date: {self.start_date},\n"
#             f"  end_date: {self.end_date},\n"
#             f"  insured_value: {self.insured_value},\n"
#             f"  prize: {self.prize},\n"
#             f"  client_id: {self.client_id}\n"
#             f"  apartment_id: {self.apartment_id}\n"
#             f")"
#         )


# Apartment Table
# class Apartment(Base):
#     __tablename__                   = "apartment"
#     id: Mapped[int]                 = mapped_column(primary_key=True)
#     apartment_number: Mapped[int]   = mapped_column(Integer(), nullable=False)
#     address: Mapped[str]            = mapped_column(String(255), nullable=False)
#     area: Mapped[int]               = mapped_column(Integer(), nullable=False)
#     client_id: Mapped[int]          = mapped_column(ForeignKey("client.id"))
#     insurance_id: Mapped[int]       = mapped_column(ForeignKey("insurance.id"))

#     def __repr__(self) -> str:
#         return (
#             f"Apartment(\n"
#             f"  id: {self.id},\n"
#             f"  insurance_number: {self.insurance_number},\n"
#             f"  address: {self.address},\n"
#             f"  area: {self.area}\n"
#             f"  client_id: {self.client_id}\n"
#             f"  insurance_id: {self.insurance_id}\n"
#             f")"
#         )

# # Client Table
# class Client(Base):
#     __tablename__                 = "client"
#     id: Mapped[int]               = mapped_column(primary_key=True)
#     name: Mapped[str]             = mapped_column(String(100), nullable=False)
#     cpf: Mapped[int]              = mapped_column(Integer(), nullable=False)
#     birthdate: Mapped[date]       = mapped_column(Date, nullable=False)           # Default Format YYYY-MM-DD
#     address: Mapped[str]          = mapped_column(String(255), nullable=True)
#     phone: Mapped[int]            = mapped_column(Integer(), nullable=False)
#     email: Mapped[str]            = mapped_column(String(255), nullable=False, unique=True)
#     # insurances: Mapped[Insurance] = relationship("Insurance", backref="client")
#     # apartment: Mapped[Apartment]  = relationship("Apartment", backref="client")

#     # Decorator
#     @property
#     def age(self) -> int:
#         today: date = date.today()
#         age: int = today.year - self.birthdate.year
#         return age

#     def __repr__(self) -> str:
#         return (
#             f"Client(\n"
#             f"  id: {self.id},\n"
#             f"  name: {self.name},\n"
#             f"  cpf: {self.cpf},\n"
#             f"  birthdate: {self.birthdate},\n"
#             f"  age: {self.age},\n"
#             f"  address: {self.address},\n"
#             f"  phone: {self.phone},\n"
#             f"  email: {self.email}\n"
#             f")"
#         )


# main.py

# TEST: Creating new Client - Success!
    # birthdate_client1_str = "1982-02-10"
    # birthdate = date.fromisoformat(birthdate_client1_str)
    # new_client = Client(
    #     name="Fulano da Silva", 
    #     cpf="12345678900",
    #     birthdate=birthdate,
    #     address="Rua X, número 123, prédio Y",
    #     phone="41987659174",
    #     email="fulano@mail.com"
    # )
    # created_client = create_client(db, new_client)
    # print(f"Cliente criado com sucesso! ID: {created_client.id}")


    # TEST: Creating another new Client - Success!
    # birthdate_client1_str = "1987-07-07"
    # birthdate = date.fromisoformat(birthdate_client1_str)
    # new_client = Client(
    #     name="Beltrano da Silva", 
    #     cpf="12345678900",
    #     birthdate=birthdate,
    #     address="Rua Y, número 321, prédio Z",
    #     phone="41987659174",
    #     email="beltrano@mail.com"
    # )
    # created_client = create_client(db, new_client)
    # print(f"Cliente criado com sucesso! ID: {created_client.id}")


# TEST: Fetch all Clients - Success!
    # clients = get_all_clients(db)

    # if clients:
    #     print("Lista de todos os clientes:")
    #     for client in clients:
    #         print(f"- {client.name} (ID: {client.id})")
    # else:
    #     print("Nenhum cliente encontrado.")


    # TEST: Fetching a Client by ID - Success!
    # client_id = 1
    # client = get_client(db, client_id)
    # if client:
    #     print(f"Cliente encontrado: {client.name}")
    # else:
    #     print(f"Cliente com ID {client_id} não encontrado.")


    # # TEST: Update Client by ID - Success!
    # client_id = 1

    # # Fetch the client to update
    # client = get_client(db, client_id)
    # if not client:
    #     print(f"Cliente com ID {client_id} não encontrado.")
    #     return

    # # Update client information
    # client.name = "Ciclano dos Santos"
    # client.email = "ciclano@mail.com"
    # client.phone = 41598763210

    # # Update the client in the database
    # update_client(db, client)

    # print(f"Cliente com ID {client_id} atualizado com sucesso!")


    # TEST: Delete Client by ID
    # client_id = 1

    # # Validate ID
    # client = get_client(db, client_id)
    # if not client:
    #     print(f"Cliente com ID {client_id} não encontrado.")
    #     return

    # # Confirm deletion
    # confirmation = input(f"Tem certeza que deseja deletar o cliente com ID {client_id}? (s/n): ")
    # if confirmation.lower() != 's':
    #     print("Cancelando a operação.")
    #     return

    # # Delete client
    # delete_client(db, client_id)
    # print("Cliente deletado com sucesso.")
