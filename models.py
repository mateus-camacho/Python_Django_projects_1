from sqlmodel import Field, SQLModel, create_engine, Relationship
from enum import Enum
from datetime import date 

# classe para o campo banco for escolher um desses, se não for um deles vai ir pro default
class Bancos(Enum):
    NUBANK = "Nubank"
    SANTANDER = "Santander"
    INTER = "Inter" 

# mesma coisa só que para status
class Status(Enum):
    ATIVO =  "Ativo"
    INATIVO = "Inativo"

class Tipo(Enum):
    ENTRADA = "Entrada"
    SAIDA = "Saida"

# aqui vai ser a tabela sql
class Conta(SQLModel, table=True):
    id: int = Field(primary_key=True)
    valor: float
    banco: Bancos = Field(default=Bancos.NUBANK)
    status: Status = Field(default=Status.ATIVO)

#aqui vai ser uma tabela que fala o histórico de transações
class Historico(SQLModel, table=True):
    id: int = Field(primary_key=True)
    conta_id: int = Field(foreign_key="conta.id")
    conta: Conta = Relationship()
    tipo: Tipo = Field(default = Tipo.ENTRADA)
    valor: float    
    data: date


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)
 

if __name__ == "__main__":
    SQLModel.metadata.create_all(engine)
