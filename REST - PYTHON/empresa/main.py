from flask import Flask, request

app = Flask(__name__)


# REST 7
@app.route('/testes/1')
def teste_query_string_1_argumento_get():
    linguagem = request.args.get('linguagem')
    return '''<h1>Linguagem informada: {}</h1>'''.format(linguagem)

@app.route('/testes/2')
def teste_query_string_2_argumento_get():
    linguagem = request.args.get('linguagem')
    framework = request.args.get('framework')
    return '''<h1>Linguagen informada: {}</h1>
              <h1>Framework informado: {}</h1>'''.format(linguagem, framework)

@app.route('/testes/3', methods=['POST'])
def testePOST():
    return jsonify ({"resp" : "Teste 3: Método POST."})

@app.route ("/testes/4", methods=['GET', 'POST'])
def teste_GET_POST() :
    return jsonify({"resp" : "Teste 4: Método GET ou POST."})


# REST 8
@app.route('/temperatura', methods=['GET', 'POST'])
def calculaTemperatura():
    celcius = int(request.form.get('celcius'))
    fahrenheit = celcius * 1.8 + 32   
    return '''<h1>A temperatura em celcius inserida foi: {}</h1>
              <h1>A temperatura em fahrenheit é: {}'''.format(celcius,  round(fahrenheit, 2))

@app.route('/notas', methods=['GET', 'POST'])
def calculaNotas():
    nota1 = int(request.form.get('nota1'))
    nota2 = int(request.form.get('nota2'))
    nota3 = int(request.form.get('nota3'))
    soma = nota1 + nota2 + nota3
    media = soma / 3
    if (media < 3): 
        return '''<h1>As notas do aluno foram: {}, {}, {}.</h1>
              <h1>A média dele é: {}.</h1>
              <h1>Ele foi REPROVADO.</h1>'''.format(nota1,nota2,nota3,media)
    if ((media >= 3) and (media < 7)): 
        return '''<h1>As notas do aluno foram: {}, {}, {}.</h1>
              <h1>A média dele é: {}.</h1>
              <h1>Ele esta de RECUPERAÇÃO.</h1>'''.format(nota1,nota2,nota3,media)
    if ((media >= 7) and (media <=10)):
        return '''<h1>As notas do aluno foram: {}, {}, {}.</h1>
              <h1>A média dele é: {}.</h1>
              <h1>Ele foi APROVADO.</h1>'''.format(nota1,nota2,nota3,media)
    else:
        return '''<h1>Notas inválidas</h1>'''

if __name__ == '__main__':
    app.run(debug= True, port=5000)