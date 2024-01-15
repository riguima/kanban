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
