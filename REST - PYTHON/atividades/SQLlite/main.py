# Importar a classe Flask, objeto request e o objeto jsonify:
from flask import Flask, request, jsonify
import sqlite3


# Criar o objeto Flask app:
app = Flask(__name__)


# Criar o banco de dados aluno caso não existe
conexao = sqlite3.connect('aluno.db', check_same_thread=False)

cursor = conexao.cursor()

sql = 'create table IF NOT EXISTS aluno('\
'idAluno integer primary key autoincrement,'\
'nome varchar(100) not null,'\
'sexo char)'

cursor.execute(sql)

# http://127.0.0.1:5000/alunos
@app.route('/alunos', methods=['GET'])
def retornar_todos_os_produtos():
    sql = 'select * from aluno'
    alunos = cursor.execute(sql)
    return alunos

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