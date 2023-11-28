# FastAPI: criar APIs em Python.
from fastapi import FastAPI, HTTPException
# Pydantic: biblioteca para validação e conversão de tipos em Python.
from pydantic import BaseModel
# SQLAlchemy: ORM (Object-Relational Mapping) para Python.
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Float
# Configuração do SQLite:
DATABASE_URL = "sqlite:///./empresa.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Declarando o modelo da tabela de trabalhadores usando SQLAlchemy:
Base = declarative_base()
class Trabalhador(Base):
    __tablename__ = "trabalhador"
    id = Column(Integer, primary_key=True, index=True)
    cpf = Column(Integer, index=True)
    nome = Column(String, index=True)
    horasTrabalhadas = Column(Integer)
    valorHora = Column(Float)

Base.metadata.create_all(bind=engine)
# Inicialização do aplicativo FastAPI:
app = FastAPI()
# Modelo Pydantic para validação de entrada:
# Pydantic: biblioteca de validação de dados mais amplamente usada para
class TrabalhadorCreate(BaseModel):
    cpf: int
    nome: str
    horasTrabalhadas : int
    valorHora: float
    
class TrabalhadorNomeCreate(BaseModel):
    nome: str
    
class TrabalhadorHorasTrabalhadasCreate(BaseModel):
    horasTrabalhadas: int

class TrabalhadorCpfCreate(BaseModel):
    cpf: int
    
class TrabalhadorValorHoraCreate(BaseModel):
    valorHora: float
    
class PagamentoCreate(BaseModel):
    nome: str
    valor: float
    
@app.post("/trabalhadores/", response_model=TrabalhadorCreate)
def criar_trabalhador(trabalhador: TrabalhadorCreate):
        db = SessionLocal() 
        db_trabalhador = Trabalhador(**trabalhador.model_dump())
        db.add(db_trabalhador)
        db.commit()
        db.refresh(db_trabalhador)
        db.close()
        return trabalhador
    
@app.get("/trabalhadores/{trabalhador_id}", response_model=TrabalhadorCreate)
def ler_trabalhador(trabalhador_id: int):
    db = SessionLocal()
    trabalhador = db.query(Trabalhador).filter(Trabalhador.id == trabalhador_id).first()
    db.close()
    if trabalhador:
        return trabalhador
    raise HTTPException(status_code=404, detail="Trabalhador não encontrado")

@app.get("/trabalhadores/", response_model=list[TrabalhadorCreate])
def listar_trabalhadores():
    db = SessionLocal()
    trabalhadores = db.query(Trabalhador).all()
    db.close()
    return trabalhadores
    
@app.put("/trabalhadores/{trabalhador_id}", response_model=TrabalhadorCreate)
def atualizar_trabalhador(trabalhador_id: int, trabalhador: TrabalhadorCreate):
    db = SessionLocal()
    db_trabalhador = db.query(Trabalhador).filter(Trabalhador.id == trabalhador_id).first()
    if db_trabalhador:
        for key, value in trabalhador.model_dump().items():
            '''
            setattr é uma função para definir atributos de objetos
            dinamicamente em tempo de execução.
            '''
            setattr(db_trabalhador, key, value)
        db.commit()
        db.refresh(db_trabalhador)
        db.close()
        return db_trabalhador
    raise HTTPException(status_code=404, detail="Trabalhador não encontrado")


@app.put("/trabalhadores/atualizarNome/{trabalhador_id}", response_model=TrabalhadorNomeCreate)
def atualizar_nome_trabalhador(trabalhador_id: int, trabalhadorNome: TrabalhadorNomeCreate):
    db = SessionLocal()
    db_trabalhador = db.query(Trabalhador).filter(Trabalhador.id == trabalhador_id).first()
    if db_trabalhador:
        for key, value in trabalhadorNome.model_dump().items():
            setattr(db_trabalhador, key, value)
        db.commit()
        db.refresh(db_trabalhador)
        db.close()
        return db_trabalhador
    raise HTTPException(status_code=404, detail="Trabalhador não encontrado.")


@app.put("/trabalhadores/atualizarCPF/{trabalhador_id}", response_model=TrabalhadorCpfCreate)
def atualizar_cpf_trabalhador(trabalhador_id: int, trabalhadorCPF: TrabalhadorCpfCreate):
    db = SessionLocal()
    db_trabalhador = db.query(Trabalhador).filter(Trabalhador.id == trabalhador_id).first()
    if db_trabalhador:
        for key, value in trabalhadorCPF.model_dump().items():
            setattr(db_trabalhador, key, value)
        db.commit()
        db.refresh(db_trabalhador)
        db.close()
        return db_trabalhador
    raise HTTPException(status_code=404, detail="Trabalhador não encontrado.")


@app.put("/trabalhadores/atualizarHorasTrabalhadas/{trabalhador_id}", response_model=TrabalhadorHorasTrabalhadasCreate)
def atualizar_horas_trabalhadas_trabalhador(trabalhador_id: int, trabalhadorHorasTrabalhadas: TrabalhadorHorasTrabalhadasCreate):
    db = SessionLocal()
    db_trabalhador = db.query(Trabalhador).filter(Trabalhador.id == trabalhador_id).first()
    if db_trabalhador:
        for key, value in trabalhadorHorasTrabalhadas.model_dump().items():
            setattr(db_trabalhador, key, value)
        db.commit()
        db.refresh(db_trabalhador)
        db.close()
        return db_trabalhador
    raise HTTPException(status_code=404, detail="Trabalhador não encontrado.")


@app.put("/trabalhadores/atualizarValorHora/{trabalhador_id}", response_model=TrabalhadorValorHoraCreate)
def atualizar_valor_hora_trabalhador(trabalhador_id: int, trabalhadorValorHora: TrabalhadorValorHoraCreate):
    db = SessionLocal()
    db_trabalhador = db.query(Trabalhador).filter(Trabalhador.id == trabalhador_id).first()
    if db_trabalhador:
        for key, value in trabalhadorValorHora.model_dump().items():
            setattr(db_trabalhador, key, value)
        db.commit()
        db.refresh(db_trabalhador)
        db.close()
        return db_trabalhador
    raise HTTPException(status_code=404, detail="Trabalhador não encontrado.")


@app.put("/trabalhadores/atualizarNome/{trabalhador_id}", response_model=TrabalhadorValorHoraCreate)
def atualizar_nome_trabalhador(trabalhador_id: int, trabalhadorValorHora: TrabalhadorValorHoraCreate):
    db = SessionLocal()
    db_trabalhador = db.query(Trabalhador).filter(Trabalhador.id == trabalhador_id).first()
    if db_trabalhador:
        for key, value in trabalhadorValorHora.model_dump().items():
            setattr(db_trabalhador, key, value)
        db.commit()
        db.refresh(db_trabalhador)
        db.close()
        return db_trabalhador
    raise HTTPException(status_code=404, detail="Trabalhador não encontrado.")


@app.delete("/trabalhadores/{trabalhador_id}", response_model=TrabalhadorCreate)
def deletar_trabalhador(trabalhador_id: int):
    db = SessionLocal()
    trabalhador = db.query(Trabalhador).filter(Trabalhador.id == trabalhador_id).first()
    if trabalhador:
        db.delete(trabalhador)
        db.commit()
        db.close()
        return trabalhador
    raise HTTPException(status_code=404, detail="Trabalhador não encontrado")
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
    
    