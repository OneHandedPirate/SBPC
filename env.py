import os

from dotenv import load_dotenv

load_dotenv()

POSTGRESQLPASSWORD = os.getenv('POSTGRESQLPASSWORD')
DJANGO_SK = os.getenv('DJANGO_SK')