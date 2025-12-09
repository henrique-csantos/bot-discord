import os
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

# Obter o token
TOKEN = os.getenv('DISCORD_TOKEN')