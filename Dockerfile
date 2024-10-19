FROM python:3.11-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY . .

RUN mkdir -p /app/data/complete /app/data/processed /app/data/raw/test /app/data/raw/train

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD ["poetry", "run", "python", "main.py"]
