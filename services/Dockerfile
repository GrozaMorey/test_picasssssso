FROM python:3.11-alpine

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

CMD ["python", "manage.py", "migrate"]
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "services.wsgi:application"]
