FROM python:3.9

WORKDIR /app

RUN pip install gunicorn==21.2.0

COPY . .

RUN pip install -r requirements.txt --no-cache-dir

CMD ["bash", "./entrypoint.sh"]