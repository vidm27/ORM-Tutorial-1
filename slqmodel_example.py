from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, create_engine


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


class Competidor(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(max_length=50, nullable=False)
    lastname: str = Field(max_length=50, nullable=False)
    gender: str = Field(max_length=15, nullable=False)
    cinturon_id: UUID = Field(foreign_key="cinturon.id", nullable=False)


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

SQLModel.metadata.create_all(engine)
