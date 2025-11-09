import mysql.connector

def test_root_db_access():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="safe123"
    )
    print(mydb) 