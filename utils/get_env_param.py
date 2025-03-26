import os

from dotenv import load_dotenv, find_dotenv
from pathlib import Path


load_dotenv()

def get_env_param(param: str):
    return os.getenv(param)