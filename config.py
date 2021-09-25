from os import path, environ

from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
DOTENV_PATH = path.join(BASE_DIR, ".env")
load_dotenv(DOTENV_PATH)
