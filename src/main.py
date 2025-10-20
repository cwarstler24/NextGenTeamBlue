import mysql.connector

connect = mysql.connector.connect(user='',
                                  password='',
                                  host='localhost',
                                  database='test_asset_management_system')

with connect.cursor() as cursor:
    result = cursor.execute("SELECT * FROM employee")

    rows = cursor.fetchall()

    for rows in rows:
        print(rows)

connect.close()