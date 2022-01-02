import os
import re
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
from os.path import join, dirname
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, flash, url_for, session, redirect
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
app = Flask(__name__)
app.secret_key = 'auth@flask'
# Conexão Postgres
DB_HOST = os.environ.get("SECRET_DB_HOST")
DB_NAME = os.environ.get("SECRET_DB_NAME")
DB_USER = os.environ.get("SECRET_DB_USER")
DB_PASS = os.environ.get("SECRET_DB_PASS")
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Verifique se o usuário está logado
    if 'loggedin' in session:
        # O usuário está logado, mostre a página inicial
        return render_template('home.html', nome=session['nome'])
    # O usuário não está logado redirecionar para a página de login
    return redirect(url_for('login'))
 

@app.route('/login/', methods=['GET', 'POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST' and 'key' in request.form and 'email' in request.form:
        
        # Variáveis ​​para fácil acesso
        email = request.form['email']
        key = request.form['key']       
        # print(email)
        # print(key)
        # Verifica se a conta existe usando Postgres
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        # Buscar um registro e retornar o resultado
        account =  cursor.fetchone()
        if account:
            key_postgres = account['key']
            # print(f'"{key_postgres}"')
            # Se a conta existir na tabela de usuários em nosso banco de dados
            if check_password_hash(key_postgres, key):
                # Criar dados da sessão, podemos acessar esses dados em outras rotas   
                session['loggedin'] = True
                session['id'] = account['id']
                session['nome'] = account['nome']
                # Redirecionar para a página principal.
                return redirect(url_for('index'))
            else:
                # Conta existe, mas a senha está incorreta.
                flash('Senha incorreta!')
        else:
            # A conta não existe 
            flash('A conta não existe!')
    return render_template('login.html')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Verifica se existem solicitações POST de "nome", "senha" e "email" (formulário enviado pelo usuário)
    if request.method == 'POST' and 'nome' in request.form and 'key' in request.form and 'email' in request.form:
        
        # Variáveis ​​para fácil acesso
        nome = request.form['nome']
        key = request.form['key']
        email = request.form['email']
        # print(nome)
        # print(key)
        # print(email)
        # Verifica se a conta existe usando Postgres
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account =  cursor.fetchone()
        # Se a conta existir, mostrar erros e verificações de validação
        if account:
            # print(account)
            flash('Essa conta já existe!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Endereço de email invalido!')
        elif not re.match(r'[A-Za-z0-9]+', key):
            flash('A senha deve conter apenas caracteres e números!')
        elif not nome or not key or not email:
            flash('Por favor, preencha o formulário!')
        else:
            # A conta não existe e os dados do formulário são válidos, agora insira uma nova conta na tabela de usuários
            _hash_key = generate_password_hash(key)
            cursor.execute("INSERT INTO users(nome, email, key) VALUES (%s,%s,%s)", (nome, email, _hash_key))
            conn.commit()
            flash('Você se registrou com sucesso!')
    elif request.method == 'POST':
        # Formulário está vazio ... (sem dados POST)
        flash('Por favor, preencha o formulário!')
    # Mostrar formulário de registro com mensagem (se houver)
    return render_template('register.html')

@app.route("/logout/")
def logout():
    # Remova os dados da sessão, isso desconectará o usuário
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('nome', None)
    return redirect(url_for('login'))
if __name__ == "__main__":
    app.run(debug=True)