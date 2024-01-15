FROM python
WORKDIR /app
COPY . .
RUN pip install pipenv
RUN pipenv requirements > requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8000
CMD [ "gunicorn", "-b", "0.0.0.0", "app:app" ]
