import os
import psycopg2 
from dotenv import load_dotenv 
from flask import Flask, request

app = Flask(__name__)

#getting database details

CREATE_STUDENT_TABLE = (
    "CREATE TABLE IF NOT EXISTS Students (Email varchar,Phone_no bigint,name varchar,class varchar,board varchar,school varchar,DOB date,password varchar);"
)

INSERT_STUDENT = "INSERT INTO Students (Email,Phone_no,name,class,board,school,DOB,password) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"

SELECT_STUDENT = "SELECT * FROM Students where email = "

load_dotenv()

db_host = os.getenv("DATABASE_HOST")
db_name = os.getenv("DATABASE_NAME")
db_user = os.getenv("DATABASE_USERNAME")
db_port = os.getenv("DATABASE_PORT")
db_pwd =  os.getenv("DATABASE_PASSWORD")

connection = psycopg2.connect(host = db_host, dbname = db_name, user = db_user, password = db_pwd, port = db_port)

@app.post("/tutor/register")
def create_student():
    data = request.get_json()
    name = data["name"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_STUDENT_TABLE)
            cursor.execute(INSERT_STUDENT, (data["Email"], data["Phone_no"], data["name"], data["class"], data["board"], data["school"], data["DOB"], data["password"]))
            connection.commit()
    return("Data created")
@app.get("/tutor/student")
def get_details():
    data = request.get_json()
    em = data["Email"]
    print(type(em))
    final = (SELECT_STUDENT +"'"+ em + "'")
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(final)
            result = cursor.fetchall()
    return(result)


# connection.close()
if __name__ == '__main__':
    app.run()
