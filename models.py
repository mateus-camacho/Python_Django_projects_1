from sqlmodel import Field, SQLModel, create_engine
from enum import Enum


# classe para o campo banco for escolher um desses, se não for um deles vai ir pro default
class Bancos(Enum):
    NUBANK = "Nubank"
    SANTANDER = "Santander"
    INTER = "Inter" 

# mesma coisa só que para status
class Status(Enum):
    ATIVO =  "Ativo"
    INATIVO = "Inativo"

# aqui vai ser a tabela sql
class Conta(SQLModel, table=True):
    id: int = Field(primary_key=True)
    valor: float
    banco: Bancos = Field(default=Bancos.NUBANK)
    status: Status = Field(default=Status.ATIVO)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)
 

if __name__ == "__main__":
    SQLModel.metadata.create_all(engine)
