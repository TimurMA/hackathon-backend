from utils.get_env_param import get_env_param

POSTGRES_USER = get_env_param("POSTGRES_USER")
POSTGRES_PASSWORD = get_env_param("POSTGRES_PASSWORD")
POSTGRES_DB = get_env_param("POSTGRES_DB")
POSTGRES_PORT = get_env_param("POSTGRES_PORT")
POSTGRES_HOST = get_env_param("POSTGRES_HOST")


def get_database_url():
    return f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
