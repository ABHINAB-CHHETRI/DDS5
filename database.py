import pymysql

timeout = 10
connection = pymysql.connect(
  charset="utf8mb4",
  connect_timeout=timeout,
  cursorclass=pymysql.cursors.DictCursor,
  db="defaultdb",
  host="drone-dispatch-system-thapar-a4f3.c.aivencloud.com",
  password="AVNS_jjQPJ7jxq9aVaNDMFBE",
  read_timeout=timeout,
  port=23916,
  user="avnadmin",
  write_timeout=timeout,
)
  
try:
  cursor = connection.cursor()
  cursor.execute("CREATE TABLE mytest (id INTEGER PRIMARY KEY)")
  cursor.execute("INSERT INTO mytest (id) VALUES (1), (2)")
  cursor.execute("SELECT * FROM mytest")
  print(cursor.fetchall())
finally:
  connection.close()