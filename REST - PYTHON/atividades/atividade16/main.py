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
DATABASE_URL = "sqlite:///./produto.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Declarando o modelo da tabela de produtos usando SQLAlchemy:
Base = declarative_base()
class Produto(Base):
    __tablename__ = "produto"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    preco = Column(Float)

Base.metadata.create_all(bind=engine)
# Inicialização do aplicativo FastAPI:
app = FastAPI()
# Modelo Pydantic para validação de entrada:
# Pydantic: biblioteca de validação de dados mais amplamente usada para
class ProdutoCreate(BaseModel):
    nome: str
    preco: float
    
@app.post("/produtos/", response_model=ProdutoCreate)
def criar_produto(produto: ProdutoCreate):
        db = SessionLocal() 
        db_produto = Produto(**produto.model_dump())
        db.add(db_produto)
        db.commit()
        db.refresh(db_produto)
        db.close()
        return produto
    
@app.get("/produtos/{produto_id}", response_model=ProdutoCreate)
def ler_produto(produto_id: int):
    db = SessionLocal()
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    db.close()
    if produto:
        return produto
    raise HTTPException(status_code=404, detail="Produto não encontrado")

@app.get("/produtos/", response_model=list[ProdutoCreate])
def listar_produtos():
    db = SessionLocal()
    produtos = db.query(Produto).all()
    db.close()
    return produtos

@app.put("/produtos/{produto_id}", response_model=ProdutoCreate)
def atualizar_produto(produto_id: int, produto: ProdutoCreate):
    db = SessionLocal()
    db_produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if db_produto:
        for key, value in produto.model_dump().items():
            '''
            setattr é uma função para definir atributos de objetos
            dinamicamente em tempo de execução.
            '''
            setattr(db_produto, key, value)
        db.commit()
        db.refresh(db_produto)
        db.close()
        return db_produto
    raise HTTPException(status_code=404, detail="Produto não encontrado")

@app.delete("/produtos/{produto_id}", response_model=ProdutoCreate)
def deletar_produto(produto_id: int):
    db = SessionLocal()
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if produto:
        db.delete(produto)
        db.commit()
        db.close()
        return produto
    raise HTTPException(status_code=404, detail="Produto não encontrado")
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
    
    