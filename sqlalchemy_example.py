from datetime import datetime
from uuid import uuid4

from sqlalchemy import String, Column, Text, DateTime, ForeignKey, Integer, Float, Table
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, relationship

# declarative base class
Base = declarative_base()


# an example mapping using the base
class Dojo(Base):
    __tablename__ = "dojo"

    id = Column(String(36), primary_key=True, default=str(uuid4()), unique=True)
    name = Column(String(50), nullable=False)
    sensei_name = Column(String(50), nullable=False)
    sensei_lastname = Column(String(50), nullable=False)
    path_logo = Column(Text, nullable=True)

    torneos = relationship("Torneo", back_populates="dojo", )

    def __repr__(self) -> str:
        return (f"Dojo(id={self.id!r}, name={self.name!r}, sensei_name={self.sensei_name!r},"
                f"sensei_lastname={self.sensei_lastname!r},path_logo={self.path_logo!r})")


class Torneo(Base):
    __tablename__ = "torneo"
    id = Column(String(36), primary_key=True, default=str(uuid4()), unique=True)
    name = Column(Text, nullable=False)
    dt_created = Column(DateTime, nullable=False, default=datetime.utcnow())
    dt_schedule = Column(DateTime, nullable=True)
    dojo_id = Column(String(36), ForeignKey("dojo.id"), nullable=False)

    dojo = relationship("Dojo", back_populates="torneo")


class Cinturon(Base):
    __tablename__ = "cinturon"
    id = Column(String(36), primary_key=True, default=str(uuid4()), unique=True)
    description = Column(String(20), nullable=False)
    range_level = Column(Integer, nullable=True)

    competidores = relationship("Competidor", back_populates="cinturon", )


class Puntaje(Base):
    __tablename__ = "puntaje"
    id = Column(String(36), primary_key=True, default=str(uuid4()), unique=True)
    value = Column(Float, nullable=False)
    dt_entry = Column(DateTime, nullable=True)
    dt_update = Column(DateTime, nullable=True)


class Competidor(Base):
    __tablename__ = "competidor"
    id = Column(String(36), primary_key=True, default=str(uuid4()), unique=True)
    name = Column(String(40), nullable=False)
    lastname = Column(String(40), nullable=False)
    gender = Column(String(15), nullable=False)

    cinturon_id = Column(String(36), ForeignKey("cinturon.id"), nullable=False)

    cinturon = relationship("Cinturon", back_populates="competidor")


class Competicion(Base):
    __tablename__ = "competicion"
    id = Column(String(36), primary_key=True, default=str(uuid4()), unique=True)
    name = Column(String(100), nullable=False)
    dt_created = Column(DateTime, nullable=False, default=datetime.utcnow())


CategoriaCompetidor = Table(
    "categoria_competidor",
    Base.metadata,
    Column("competidor_id", ForeignKey("competidor.id"), nullable=False),
    Column("categoria_id", ForeignKey("categoria.id"), nullable=False),
    Column("puntaje_id", ForeignKey("puntaje.id"), nullable=True),
    Column("round", String(20), nullable=False),
    Column("position", Integer, nullable=True)
)

CategoriaCinturon = Table(
    "categoria_cinturon",
    Base.metadata,
    Column("cinturon_id", ForeignKey("cinturon.id"), nullable=False),
    Column("categoria_id", ForeignKey("categoria.id"), nullable=False)
)


class Categoria(Base):
    __tablename__ = "categoria"
    id = Column(String(36), primary_key=True, default=str(uuid4()), unique=True)
    description = Column(String(50), nullable=False)
    age_min = Column(Integer, nullable=False)
    age_max = Column(Integer, nullable=False)
    competicion_id = Column(String(36), ForeignKey("competidor.id"), nullable=False)
    torneo_id = Column(String(36), ForeignKey("torneo.id"), nullable=False)
    competidores = relationship("Competidor", secondary=CategoriaCompetidor, backref="competidores")
    cinturones = relationship("Cinturon", secondary=CategoriaCinturon, backref='cinturones')


sqlite_file_name = "dojo_alchemy.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True, future=True)

Base.metadata.create_all(engine)
