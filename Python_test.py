import pyodbc
import psycopg2
# sql_server_conn = pyodbc.connect('DRIVER={};SERVER=your_server;DATABASE=Test_db;UID=arjunsubash;PWD=Arjun@1996')
sql_server_conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=sql;DATABASE=test_db;UID=arjunsubash;PWD=Arjun@1996;KeyFile=C:\Program Files\Microsoft SQL Server\Client SDK\ODBC\180\KeyFile\1033')
sql_server_cursor = sql_server_conn.cursor()
postgresql_conn = psycopg2.connect(host="localhost", database="Test_db", user="arjunsubash", password="Arjun@1996")
postgresql_cursor = postgresql_conn.cursor()
sql_server_cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
tables = sql_server_cursor.fetchall()
for table in tables:
    table_name = table[0]
    sql_server_cursor.execute(f"SELECT TOP 1 * FROM {table_name}")
    columns = [column[0] for column in sql_server_cursor.description]
    column_string = ', '.join([f"{column} varchar" for column in columns])
    postgresql_cursor.execute(f"CREATE TABLE {table_name} ({column_string})")
    sql_server_cursor.execute(f"SELECT * FROM {table_name}")
    rows = sql_server_cursor.fetchall()
    for row in rows:
        postgresql_cursor.execute(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s']*len(columns))})", row)
postgresql_conn.commit()
postgresql_cursor.close()
postgresql_conn.close()

sql_server_cursor.close()
sql_server_conn.close()