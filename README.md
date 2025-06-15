# Sistema de Cadastro de Usuários

Este projeto é um sistema de cadastro de usuários desenvolvido em Django, onde um professor pode cadastrar disciplinas e alunos. Os dados são armazenados temporariamente em um arquivo JSON.

## Estrutura do Projeto

```
sistema-cadastro
├── cadastro
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── migrations
│       └── __init__.py
├── sistema_cadastro
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── temp_storage
│   └── dados_temp.json
├── manage.py
└── README.md
```

## Instalação

1. Clone o repositório:
   ```
   git clone 
   ```
2. Navegue até o diretório do projeto:
   ```
   cd sistema-cadastro
   ```
3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

## Uso

1. Execute as migrações:
   ```
   python manage.py migrate
   ```
2. Inicie o servidor de desenvolvimento:
   ```
   python manage.py runserver
   ```
3. Acesse o sistema em seu navegador através de `http://127.0.0.1:8000/`.

## Funcionalidades

- Cadastro de professores
- Cadastro de disciplinas
- Cadastro de alunos
- Armazenamento temporário de dados em JSON
