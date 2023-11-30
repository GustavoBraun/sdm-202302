# Importar a classe Flask, objeto request e o objeto jsonify:
from flask import Flask
from flask_restx import reqparse, abort, Api, Resource, fields
import json
import sqlite3


app = Flask(__name__)
api = Api(app,
          version='1.0',
          title='Atividade SQLite',
          description='Atividade SQLite')

# Criar o banco de dados aluno caso não existe
conexao = sqlite3.connect('aluno.db', check_same_thread=False)

cursor = conexao.cursor()

sql = 'create table IF NOT EXISTS aluno('\
'matricula integer primary key autoincrement,'\
'nome varchar(100),'\
'sexo char,'\
 'cpf varchar(11),'\
 'endereco varchar(50),'\
 'email varchar(50),'\
 'celular varchar(11),'\
 'nota char)'

sqlProdutos = 'create table IF NOT EXISTS produtos('\
'id integer primary key autoincrement,'\
'nome varchar(100),'\
'descricao varchar(40),'\
 'fornecedor varchar(11),'\
 'preco integer,'\
 'quantidade integer)'

sqlDrop = 'drop table produtos'
cursor.execute(sqlDrop)
campos_obrigatorios_para_insercao_aluno = api.model('Inserção aluno', {
     'matricula' : fields.Integer(required = True, description = 'Matricula do aluno'),
     'nome' : fields.String(required = True, description = 'Nome do aluno'),
     'sexo' : fields.String(required = True, description = 'Genero do aluno'),
     'cpf' : fields.String(required = True, description = 'CPF do aluno'),
     'endereco' : fields.String(required = True, description = 'Endereço do aluno'),
     'email' : fields.String(required = True, description = 'E-mail do aluno'),
     'celular' : fields.String(required = True, description = 'Telefone de contato do aluno'),
     'nota' : fields.String(required = True, description = 'Nota que o aluno tirou'),
    })

campos_obrigatorios_para_atualizacao_aluno = api.model('Atualização aluno', {
     'matricula' : fields.Integer(required = False, description = 'Matricula do aluno'),
     'nome' : fields.String(required = True, description = 'Nome do aluno'),
     'sexo' : fields.String(required = True, description = 'Genero do aluno'),
     'cpf' : fields.String(required = True, description = 'CPF do aluno'),
     'endereco' : fields.String(required = True, description = 'Endereço do aluno'),
     'email' : fields.String(required = True, description = 'E-mail do aluno'),
     'celular' : fields.String(required = True, description = 'Telefone de contato do aluno'),
     'nota' : fields.String(required = True, description = 'Nota que o aluno tirou'),
    })

campos_obrigatorios_para_insercao_produto = api.model('Inserção produto', {
     'id' : fields.Integer(required = True, description = 'Id do produto'),
     'nome' : fields.String(required = True, description = 'Nome do produto'),
     'descricao' : fields.String(required = True, description = 'Descrição do produto'),
     'fornecedor' : fields.String(required = True, description = 'Fornecedor do produto'),
     'preco' : fields.Integer(required = True, description = 'Preço do produto'),
     'quantidade' : fields.Integer(required = True, description = 'Quantidade em estoque'),
     })
campos_obrigatorios_para_atualizacao_produto = api.model('Atualização produto', {
     'id' : fields.Integer(required = True, description = 'Id do produto'),
     'nome' : fields.String(required = True, description = 'Nome do produto'),
     'descricao' : fields.String(required = True, description = 'Descrição do produto'),
     'fornecedor' : fields.String(required = True, description = 'Fornecedor do produto'),
     'preco' : fields.Integer(required = True, description = 'Preço do produto'),
     'quantidade' : fields.Integer(required = True, description = 'Quantidade em estoque'),
     })

parserEmpresa = reqparse.RequestParser()
parserEmpresa.add_argument('id', type = int, help = 'Id do produto')
parserEmpresa.add_argument('nome', type = str, help = 'Nome do produto')
parserEmpresa.add_argument('descricao', type = str, help = 'Descrição do produto')
parserEmpresa.add_argument('fornecedor', type = str, help = 'Fornecedor do produto')
parserEmpresa.add_argument('preco', type = int, help = 'Preço do produto')
parserEmpresa.add_argument('quantidade', type = int, help = 'Quantidade de itens em estoque')

parserAlunos = reqparse.RequestParser()
parserAlunos.add_argument('matricula', type = int, help = 'Matricula identificadora do aluno.')
parserAlunos.add_argument('nome', type = str, help = 'Nome do aluno.')
parserAlunos.add_argument('sexo', type = str, help = 'Sexo do aluno')
parserAlunos.add_argument('cpf', type = str, help = 'CPF do aluno')
parserAlunos.add_argument('endereco', type = str, help = 'Endereço do aluno')
parserAlunos.add_argument('email', type = str, help = 'E-mail do aluno')
parserAlunos.add_argument('celular', type = str, help = 'Telefone de contato do aluno')
parserAlunos.add_argument('nota', type = str, help = 'Nota do aluno.')

cursor.execute(sql)
cursor.execute(sqlProdutos)

@api.route('/produtos/<id>')
@api.doc(params={'id' : 'Id do produto'})
class Produto(Resource):
    @api.doc(response={200: 'Produto retornado.'})
    def get(self, id):
         sql = 'select * from produtos where id = ?'
         return json.dumps(list(cursor.execute(sql, id)))
    
    @api.doc(response={200: 'Produto alterado.'})
    @api.expect(campos_obrigatorios_para_atualizacao_produto)
    def put(self, id):
         args = parserEmpresa.parse_args()
         sql = 'update produtos '\
               'set nome = ?, descricao = ?, fornecedor = ?, preco = ?, quantidade = ?'\
               'where id = ?'
         cursor.execute(sql, [args['nome'], args['descricao'], args['fornecedor'], args['preco'], args['quantidade'], id])
         return 'Produto alterado.'

         

    @api.doc(response={204 : 'Produto removido'})
    def delete(self, id):
         sql = 'delete from produtos where id = ?'
         cursor.execute(sql, id)
         return 'Produto removido'
    

@api.route('/produtos')
class ListaProdutos(Resource):
    @api.doc(response={200: 'Produtos retornados.'})
    def get(self):
         sql = 'select * from produtos'
         produtos = cursor.execute(sql)
         return json.dumps(list(produtos))
    
    @api.doc(response={201: 'Produto criado.'})
    @api.expect(campos_obrigatorios_para_insercao_produto)
    def post(self):
         args = parserEmpresa.parse_args()
         sql = 'insert into produtos (id, nome,  descricao, fornecedor, preco, quantidade) values(?, ?, ?, ?, ?, ?)'
         cursor.execute(sql, [args['id'], args['nome'], args['descricao'], args['fornecedor'], args['preco'], args['quantidade']])
         return 'Produto criado.'
    

@api.doc(params={'matricula' : 'Matricula do aluno'})
@api.route('/alunos/<matricula>')
class Aluno(Resource):
    @api.doc(response={200: 'aluno retornado.'})
    def get(self, matricula):
            sql = 'select * from aluno where matricula = ?'
            aluno = cursor.execute(sql, matricula)
            return json.dumps(list(aluno))
    
    @api.doc(response={200: 'Aluno alterado'})
    @api.expect(campos_obrigatorios_para_atualizacao_aluno)
    def put(self, matricula):
         args = parserAlunos.parse_args()
         sql = 'update aluno '\
                'set nome = ?, sexo = ?, cpf = ?, endereco = ?, email = ?, celular = ?, nota = ?'\
                'where matricula = ?'
         cursor.execute(sql, [args['nome'], args['sexo'], args['cpf'], args['endereco'], args['email'], args['celular'], args['nota'], matricula])
         return 'Aluno atualizado'
    
    @api.doc(response={204: 'Aluno removido'})
    def delete(self, matricula):
         sql = 'delete from aluno where matricula = ?'
         cursor.execute(sql, matricula)
         return 'Aluno removido'

@api.route('/alunos')
class ListaAluno(Resource):
    @api.doc(response={200: 'alunos retornados'})
    def get(self):
        sql = 'select * from aluno'
        alunos = list(cursor.execute(sql))
        jsonOutput = json.dumps(alunos)
        return jsonOutput
    
    @api.doc(response={201: 'Aluno criado.'})
    @api.expect(campos_obrigatorios_para_insercao_aluno)
    def post(self):
        args = parserAlunos.parse_args()
        sql = 'insert into aluno(matricula, nome, sexo, cpf, endereco, email, celular, nota) values(?, ?, ?, ?, ?, ?, ?, ?)'
        cursor.execute(sql, [args['matricula'], args['nome'], args['sexo'], args['cpf'], args['endereco'], args['email'], args['celular'], args['nota']])
        conexao.commit()
        return 201

if __name__ == '__main__':
# Executar app no modo debug (default) na porta 5000 (default):
    app.run(debug = True, port = 5000)