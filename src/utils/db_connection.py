import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
  try:
    conn = psycopg2.connect(
      host = os.getenv("DB_HOST"),
      port = os.getenv("DB_PORT"),
      database = os.getenv("DB_NAME"),
      user = os.getenv("DB_USER"),
      password = os.getenv("DB_PASSWORD")
    )

    return conn
  except Exception as e:
    print(f"Error connecting database: {e}")
    return None