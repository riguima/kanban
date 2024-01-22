# Kanban

[![Presentation](https://99freelas.s3-sa-east-1.amazonaws.com/portfolios/imagens/original/1641617/d77d7bdc-1ddd-4831-a2b1-eff8cb72389b/screenshot.png?id=4052855&token=d77d7bdc-1ddd-4831-a2b1-eff8cb72389b&nome=screenshot&type=.png)](https://youtu.be/WXxB4UhQImk)

Aplicação simples de Kanban

## Instalação

Segue script de instalação:

```
git clone https://github.com/riguima/kanban
cd kanban
pip install pipenv
pipenv requirements > requirements.txt
pip install -r requirements.txt
```

Agora renomeie o arquivo `.base.config.toml` para `.config.toml` e altere as configurações necessárias:

- `DATABASE_URI` = A URL do banco de dados, exemplo com postgres: `postgresql://username:password@localhost:5432/database`
- `SECRET_KEY` = Chave secreta, utilize o site `https://djecrety.ir/` para gerar uma chave

Rode com `gunicorn -b 0.0.0.0 app:app` ou utilizando Docker:

```
sudo docker build -t kanban .
sudo docker run --name kanban -p 8000:8000 -d kanban
```

Acesse `http://localhost:8000` para acessar o Kanban

## API

Todos os campos devem ser passados em formato `JSON`, exceto para os métodos `GET` e `DELETE`, que devem ser passados como argumentos de url, segue os endpoints:

- `/user`
    - `POST` = Campos: `name`, `email`, `password`, `photo` (Opcional).
    - `GET` = Campos: `token`.
    - `PUT` = Campos: `token`, `name`, `email`, `password`, `photo` (Opcional), `cards_ids`.
    - `DELETE` = Campos: `token`.
- `/card`
    - `POST` = Campos: `token`, `title`, `description` (Opcional), `category_id`.
    - `GET` = Campos: `token`.
    - `PUT` = Campos: `token`, `id`, `status`, `title`, `description` (Opcional), `category_id`.
    - `DELETE` = Campos: `token`, `id`.
- `/card/<card_id>`
    - `GET` = Campos: `token`.
- `/category`
    - `POST` = Campos: `token`, `name`.
    - `GET` = Campos: `token`.
    - `PUT` = Campos: `token`, `id`, `name`.
    - `DELETE` = Campos: `token`, `id`.
- `/category/<category_id>`
    - `GET` = Campos: `token`.
