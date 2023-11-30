# Importar a classe Flask, objeto request e o objeto jsonify:
from flask import Flask, request, jsonify
from flask_restful import reqparse, Api, Resource
import sqlite3


# Criar o objeto Flask app:
app = Flask(__name__)

api = Api(app)

# Criar o banco de dados aluno caso não existe
conexao = sqlite3.connect('aluno.db', check_same_thread=False)

cursor = conexao.cursor()

sql = 'create table IF NOT EXISTS aluno('\
'matricula integer primary key autoincrement,'\
'nome varchar(100) not null,'\
'sexo char,'\
 'cpf varchar(11),'\
 'endereco varchar(50),'\
 'email varchar(50),'\
 'celular varchar(11),'\
 'nota char)'

parserAlunos = reqparse.RequestParser()
parserAlunos.add_argument('matricula', type = int, help = 'Matricula identificadora do aluno.')
parserAlunos.add_argument('nome', type = str, help = 'Nome do aluno.')
parserAlunos.add_argument('sexo', type = str, help = 'Sexo do aluno')
parserAlunos.add_argument('cpf', type = str, help = 'CPF do aluno')
parserAlunos.add_argument('endereco', type = str, help = 'Endereço do aluno')
parserAlunos.add_argument('celular', type = str, help = 'Telefone de contato do aluno')
parserAlunos.add_argument('nota', type = str, help = 'Nota do aluno.')

cursor.execute(sql)

class Aluno(Resource):
    def get(self):
        sql = 'select * from aluno'
        alunos = cursor.execute(sql)
        return alunos 

    def post(self):
        args = parserAlunos.parse_args()
        sql = 'insert into aluno(matricula, nome, sexo, cpf, endereco, email, celular, nota) values(?, ?, ?, ?, ?, ?, ?, ?)'
        cursor.execute(sql, [args['matricula'], args['nome'], args['sexo'], args['cpf'], args['endereco'], args['email'], args['celular'], args['nota']])
        conexao.commit()
        
@app.route('/alunos/<int:idAluno>', methods=['GET'])
def retornar_dados_do_produto_informado(idAluno):
    sql = 'select * from aluno where idAluno = ?'
    aluno = cursor.execute(sql, idAluno)
    return aluno

# http://127.0.0.1:5000/produtos/cinto/45.67
@app.route('/alunos/<string:nome>/<string:sexo>', methods=['POST'])
def inserir_produto(nome, sexo):
    sql = 'insert into aluno(nome, sexo) values(?, ?)'
    cursor.execute(sql, [nome, sexo])
    conexao.commit()
    return 'Aluno {} de sexo {} inserido com sucesso.'.format(nome, sexo)

# http://127.0.0.1:5000/produtos/camisa/10.00
# http://127.0.0.1:5000/produtos/camisa/-10.00
@app.route('/produtos/<string:nome>/<float(signed=True):preco>',methods=['PATCH'])
def alterar_preco_do_produto(nome, preco):
    resp = {'produto': '', 'preco': None}
    for produto in produtos:
        if produto['nome'] == nome:
            produto['preco'] += preco
            resp = produto
    return jsonify(resp)
# http://127.0.0.1:5000/produtos/camisa
@app.route('/produtos/<string:nome>', methods=['DELETE'])
def remover_produto(nome):
    for i, produto in enumerate(produtos):
        if produto['nome'] == nome:
            del produtos[i]
    return jsonify({'produtos': produtos})

if __name__ == '__main__':
# Executar app no modo debug (default) na porta 5000 (default):
    app.run(debug = True, port = 5000)