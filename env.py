import os

from dotenv import load_dotenv

load_dotenv()

POSTGRESQLPASSWORD = os.getenv('POSTGRESQLPASSWORD')