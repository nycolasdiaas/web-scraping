import psycopg2
import psycopg2.extras
# from config_user_dta import config
import datetime

conn = psycopg2.connect(
    database='dbTeste', user='postgres', host='localhost', port='5432', password='3002'
)

cursor = conn.cursor()

cursor.execute("SELECT * FROM dw.reclame_aqui")


def send_csv_to_psql(connection,csv,table_):
    sql = """COPY %s FROM STDIN WITH CSV HEADER DELIMITER AS ','"""
    file = open(csv, "r")
    table = table_
    with connection.cursor() as cur:
        cur.execute("truncate " + table + ";")  #avoiding uploading duplicate data!
        cur.copy_expert(sql=sql % table, file=file)
        connection.commit()
    return connection.commit()

send_csv_to_psql(conn,'C:\Projetos\Selenium-scraper\data\data-2023-01-23.csv','dw.reclame_aqui')