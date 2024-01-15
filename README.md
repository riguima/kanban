# Kanban

Aplicação simples de Kanban

# Instalação

Segue script de instalação:

```
git clone https://github.com/riguima/kanban
cd kanban
pip install pipenv
pipenv requirements > requirements.txt
pip install -r requirements.txt
```

Rode com `gunicorn -b 0.0.0.0 app:app` ou utilizando Docker:

```
sudo docker build -t kanban .
sudo docker run --name kanban -p 8000:8000 -d kanban
```

Todos os campos devem ser passados em formato `JSON`, segue os endpoints:

- `/user`
    - `POST` = Campos: `name`, `email`, `password`, `photo` (Opcional).
    - `GET` = Campos: `token`.
    - `PUT` = Campos: `token`, `name`, `email`, `password`, `photo`, `cards_ids`.
    - `DELETE` = Campos: `token`.
- `/card`
    - `POST` = Campos: `token`, `title`, `description`, `category_id`.
    - `GET` = Campos: `token`.
    - `PUT` = Campos: `token`, `id`, `status`, `title`, `description`, `category_id`.
    - `DELETE` = Campos: `token`, `id`.
- `/card/<card_id>`
    - `GET` = Campos: `token`.
- `/card-category`
    - `POST` = Campos: `token`, `name`.
    - `GET` = Campos: `token`.
    - `PUT` = Campos: `token`, `id`, `name`.
    - `DELETE` = Campos: `token`, `id`.
- `/card-category/<card_category_id>`
    - `GET` = Campos: `token`.
