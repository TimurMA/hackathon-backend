```
git clone git@github.com:TimurMA/skillsync-backend.git
cd skillsync-backend
```

### Запустить контейнер с postgres:

```
docker compose up -d
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
