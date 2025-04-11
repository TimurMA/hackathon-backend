FROM python:3.10.11 as builder

ARG DB
ARG DB_USER
ARG DB_PASSWORD
ARG DB_NAME
ARG DB_HOST
ARG DB_PORT

ENV DB=${DB}
ENV DB_USER=${DB_USER}
ENV DB_PASSWORD=${DB_PASSWORD}
ENV DB_NAME=${DB_NAME}
ENV DB_HOST=${DB_HOST}
ENV DB_PORT=${DB_PORT}
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /webserver

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --user --no-cache-dir -r requirements.txt

FROM python:3.10.11-slim

WORKDIR /webserver

COPY --from=builder /root/.local /root/.local
COPY --from=builder /webserver/requirements.txt .
COPY . .

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN echo "DB: $DB" && \
    echo "DB_USER: $DB_USER" && \
    echo "DB_NAME: $DB_NAME" && \
    echo "DB_HOST: $DB_HOST" && \
    echo "DB_PORT: $DB_PORT"


EXPOSE 8080

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8080"]
