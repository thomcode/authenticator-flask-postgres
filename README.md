# Flask + PostgreSQL + Autenticador Hash

O que é isso?
-------------

> Este é um autenticador Python/Flask/PostgreSQL simples destinado a fornecer um exemplo funcional de login e registro de usuarios. O objetivo desse autenticador e fornecer uma base para os desenvolvedores desenvolverem outros aplicativos.

O que é hash?
-------------

> É um algoritmo matemático que transforma qualquer bloco de dados em uma série de caracteres de comprimento fixo. 

Como usar isso?
---------------

1. Crie seu banco de dados e tabela conforme está no arquivo `users.sql`.
2. Preencha as informações relevantes no arquivo `.env_config`, como o segredo do seu banco do dados, usuario, senha e o servidor PostgreSQL.
3. Renomear arquivo `.env_config` para `.env` para voltar a formato original.
4. Execute `pip install -r requirements.txt` para instalar as dependências.
5. Execute `python app.py`.
6. Navegue para http://127.0.0.1:5000/ em seu navegador.

Teste
---------------

1. Crie uma conta.
1. Tente fazer login com a conta que você criou.