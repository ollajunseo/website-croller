import mysql.connector
import csv

# MySQL 서버에 연결
connection = mysql.connector.connect(
    host="localhost",
    user="user",
    password="12345",
    database="project"
)

if connection.is_connected():
    print("데이터 베이스에 연결되었습니다.")

    cursor = connection.cursor()

    with open('C:/Users/bid/PycharmProjects/pythonProject/data_경기_토목.csv', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        for row in csv_reader:
            sql_query = """
            INSERT INTO company_info (company_nm, Business_num, company_section, company_boss, company_address, address_num, company_phone)
            VALUES (%s, %s, %s, %s, %s, %s ,%s)
            """
            cursor.execute(sql_query, row)

    connection.commit()

    cursor.close()
    connection.close()
    print("MySQL 연결을 종료합니다.")
else:
    print("MySQL 연결에 실패하였습니다.")
