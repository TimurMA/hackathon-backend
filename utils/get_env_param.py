import os

from dotenv import load_dotenv, find_dotenv
from pathlib import Path

env_file = Path('.env.dev')

if env_file.exists():
    load_dotenv(env_file)



def get_env_param(param: str):
    return os.getenv(param)