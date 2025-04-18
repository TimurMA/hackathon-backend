```
git clone git@github.com:TimurMA/skillsync-backend.git
cd skillsync-backend
```

### Запустить контейнер с postgres и бэкендом:
(с докерхаба)
```
docker compose up -d
```
или (с докерфаила)

```
docker compose -f docker-compose-dev.yml up -d
```
### Для отладки:

#### Запустить контейнер с postgres:

```
docker compose -f for-backend.yml up -d
```
#### Применить миграции:

```
alembic upgrade head
```

#### Запустить веб сервер:

```
uvicorn app.main:app --reload --port=8080
```

locahost:8080/docs - Свагер
