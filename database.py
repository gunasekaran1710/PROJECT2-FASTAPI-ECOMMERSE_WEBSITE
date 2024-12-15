import psycopg2
from psycopg2.extras import RealDictCursor
try:
    conn=psycopg2.connect(host='localhost',user='postgres',database='ecommerse',password='password123',cursor_factory=RealDictCursor)
    cursor=conn.cursor()
    print('database connected successfully')
except Exception as error:
    print('error on database connection')
    print('error',error)