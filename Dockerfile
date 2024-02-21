FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim

WORKDIR /app

RUN pip install poetry==1.6.1

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY . ./

RUN chmod +x ./start_app.sh

EXPOSE 8000

CMD ["./start_app.sh"]