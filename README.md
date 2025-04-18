```
git clone git@github.com:TimurMA/skillsync-backend.git
cd skillsync-backend
```

### Запустить контейнер с postgres и бэкендом:

```
docker compose up -d (с докерхаба)
```
или

```
docker compose -f docker-compose-dev.yml up -d (с докерфаила)
```

### Запустить контейнер с postgres:

```
docker compose -f for-backend.yml up -d
```
### Применить миграции:

```
alembic upgrade head
```

### Запустить веб сервер:

```
uvicorn app.main:app --reload --port=8080
```

locahost:8080/docs - Свагер
