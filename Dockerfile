FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p static media

RUN python manage.py collectstatic --noinput

COPY . .

EXPOSE 8000

CMD ["gunicorn", "domanitiinterrogo.wsgi"]