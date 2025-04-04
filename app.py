from flask import Flask, request, jsonify, render_template

import sqlite3
from flash_cors import CORS

app = Flask(__name__)
CORS(app)

def init_db():
    with sqlite3.connect('database.db') as conn:
        
        conn.execute("""CREATE TABLE IF NOT EXISTS livros(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            categoria TEXT NOT NULL,
            autor TEXT NOT NULL,
            imagem_url TEXT NOT NULL
            )""")
        print("Banco de Dados Criado!")

init_db()

@app.route('/') #O @ é um facilidador na criação de rotas
def home_page():
    return render_template('index.html')

#-------Rota POST------------
@app.route('/doar', methods=['POST'])
def doar():

    dados = request.get_json() #permite o acesso e como será entregue

    titulo = dados.get('titulo')
    categoria = dados.get('categoria')
    autor = dados.get('autor')
    imagem_url = dados.get('imagem_url')

    #ou usa o if not titulo or not categoria or not autor or not imagem_url:
    
    if not all([titulo,categoria,autor,imagem_url]): #all é pra pegar todos com referencia, é pra deixar mais limpo o código
        return jsonify({'erro':'Todos os campos são obrigatórios'}), 400 #formato que a menagem retorna, no caso Json

    with sqlite3.connect('database.db') as conn:
        conn.execute(f"""INSERT INTO livros (titulo, categoria, autor, imagem_url) VALUES (?,?,?,?) 
            """, (titulo, categoria, autor, imagem_url)) #para se previnir contra um possivel SQL injector
            
        conn.commit() #salva os dados que foram inseridos

        return jsonify({"mensagem":"Livro cadastrado com sucesso"}), 201

#---------Rota GET-------------------
@app.route('/livros',methods=['GET'])
def listar_livros():
    with sqlite3.connect('database.db') as conn:
        livros = conn.execute("SELECT * FROM livros").fetchall() #pega tudo que for exibido no banco de dados, em formato tupla

    livros_formatados = []

    for livro in livros: #percorre a lista
        dicionario_livros = {
            "id": livro[0],
            "titulo": livro[1],
            "categoria": livro[2],
            "autor": livro[3],
            "imagem_url": livro[4]
        }
        livros_formatados.append(dicionario_livros) #guarda os itens após organiza-lôs(adiciona do dicionario_livros no livros_formatados)
    return jsonify(livros_formatados)


if __name__ == '__main__':
  app.run(debug=True) #roda o que está em home_page, é uma segurança a mais