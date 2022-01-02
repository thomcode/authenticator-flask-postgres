import re
import psycopg2
import psycopg2.extras
from flask import Flask, render_template, request, flash
app = Flask(__name__)
app.secret_key = 'auth@flask'
# Conexão Postgres
DB_HOST = "localhost"
DB_NAME = 'authenticator_flask'
DB_USER = 'postgres'
DB_PASS = 'devmis@1'
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Verifica se existem solicitações POST de "nome", "senha" e "email" (formulário enviado pelo usuário)
    if request.method == 'POST' and 'nome' in request.form and 'key' in request.form and 'email' in request.form:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # Variáveis ​​para fácil acesso
        nome = request.form['nome']
        key = request.form['key']
        email = request.form['email']
        print(nome)
        print(key)
        print(email)
        # Verifica se a conta existe usando Postgres
        cursor.execute('SELECT * FROM users WHERE = %s', (nome,))
        account =  cursor.fetchone()´
        print(account)
        # Se a conta existir, mostrar erros e verificações de validação
        if account:
            flash('Essa conta já existe!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Endereço de email invalido!')
        elif not re.match(r'[A-Za-z0-9]+', nome):
            flash('O nome de usuário deve conter apenas caracteres e números!')
        elif not nome or not key or not email:
            flash('Por favor, preencha o formulário!')
        else:
            # A conta não existe e os dados do formulário são válidos, agora insira uma nova conta na tabela de usuários
            cursor.execute("INSERT INTO users(nome, email, key) VALUES (%s,%s,%s)", (nome, email, _ha))
    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)