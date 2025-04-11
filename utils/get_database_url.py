from utils.get_env_param import get_env_param

DB_USER = get_env_param("DB_USER")
DB_PASS = get_env_param("DB_PASSWORD")
DB_NAME = get_env_param("DB_NAME")
DB_PORT = get_env_param("DB_PORT")
DB_HOST = get_env_param("DB_HOST")


def get_database_url():
    return f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
