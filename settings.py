import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://demowebshop.tricentis.com/")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
