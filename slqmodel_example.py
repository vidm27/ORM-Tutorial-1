from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, create_engine, Session, select


class Dojo(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(nullable=False, max_length=50)
    sensei_name: str = Field(nullable=False, max_length=50)
    sensei_lastname: str = Field(nullable=False, max_length=50)
    path_logo: str


class Torneo(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str
    dt_created: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    dt_schedule: datetime

    id_dojo: Optional[UUID] = Field(default=None, foreign_key="dojo.id")


class Cinturon(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    description: str = Field(nullable=False, max_length=20)
    range_level: str = Field(max_length=20)


class Puntaje(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    puntaje: float
    dt_entry: datetime
    dt_update: datetime


# MANY TO MANY
class Competidor(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(max_length=50, nullable=False)
    lastname: str = Field(max_length=50, nullable=False)
    gender: str = Field(max_length=15, nullable=False)
    cinturon_id: Optional[UUID] = Field(default=None, foreign_key="cinturon.id")


class Competicion(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(max_length=100, nullable=False)
    dt_created: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class Categoria(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    description: str = Field(max_length=50, nullable=False)
    age_min: int = Field(nullable=False)
    age_max: int = Field(nullable=False)
    competicion_id: UUID = Field(foreign_key="competicion.id", nullable=False)
    torneo_id: UUID = Field(foreign_key="torneo.id", nullable=False)


class CategoriaCompetidor(SQLModel, table=True):
    categoria_id: Optional[UUID] = Field(default=None, foreign_key="categoria.id", primary_key=True)
    competidor_id: Optional[UUID] = Field(default=None, foreign_key="competidor.id", primary_key=True)
    puntaje_id: Optional[UUID] = Field(default=None, foreign_key="puntaje.id", primary_key=True)
    round: str
    position: int


class CategoriaCinturon(SQLModel, table=True):
    cinturon_id: Optional[UUID] = Field(default=None, foreign_key="cinturon.id", primary_key=True)
    categoria_id: Optional[UUID] = Field(default=None, foreign_key="categoria.id", primary_key=True)


sqlite_file_name = "dojo.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_cinturones():
    cinturones = [
        "blanco",
        "amarillo",
        "anaranjado",
        "verde",
        "morado",
        "chocolate",
        "negro"
    ]
    session = Session(engine)
    for cinturon in cinturones:
        current_cinturon = Cinturon(description=cinturon, range_level="basic")
        print(f"Creating Cinturon: {current_cinturon}")
        session.add(current_cinturon)

    session.commit()
    session.close()


def create_competidor():
    with Session(engine) as session:
        statement = select(Cinturon).where(Cinturon.description == "blanco")
        result = session.exec(statement)
        cinturo = result.first()

        competidor_1 = Competidor(name="Julio", lastname="Cesar", gender="masculino", cinturon_id=cinturo.id)
        competidor_2 = Competidor(name="Rosa", lastname="Purpura", gender="femenino", cinturon_id=cinturo.id)
        competidor_3 = Competidor(name="Juanito", lastname="Rosales", gender="masculino", cinturon_id=cinturo.id)

        session.add(competidor_1)
        session.add(competidor_2)
        session.add(competidor_3)

        session.commit()


def update_competidor():
    with Session(engine) as session:
        statement = select(Competidor).where(Competidor.name == "Juanito")
        result = session.exec(statement)
        competidor = result.first()
        print(f"Competidor: {competidor}")
        competidor.name = "Canelo"
        session.add(competidor)
        session.commit()
        session.refresh(competidor)
        print(f"Updated competidor: {competidor}")


def limit_competidores():
    with Session(engine) as session:
        statement = select(Competidor).limit(3)
        result = session.execute(statement)
        competidores = result.all()
        for competidor in competidores:
            print(f"Competidor: {competidor}")


def delete_competidor():
    with Session(engine) as session:
        statement = select(Competidor).where(Competidor.name == "Canelo")
        result = session.exec(statement)
        competidor = result.first()

        session.delete(competidor)
        session.commit()


if __name__ == '__main__':
    # SQLModel.metadata.create_all(engine)
    # create_cinturones()
    # create_competidor()
    # update_competidor()
    # limit_competidores()
    delete_competidor()