from pathlib import Path 
from dotenv import load_dotenv
import os

path_to_env = Path('.') / '.env'
load_dotenv(dotenv_path=path_to_env)


class Config:
    SERVER = os.getenv('SERVER')
    SECRET_KEY = os.getenv('SECRET_KEY')
