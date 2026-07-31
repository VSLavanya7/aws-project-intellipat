from flask import Flask, render_template, request
import pymysql
from config import *

app = Flask(__name__)


def get_connection():
    return pymysql.connect(
        host=customhost,
        user=customuser,
        password=custompass,
        database=customdb,
        port=customport
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/getemployee", methods=["POST"])
def get_employee():

    empid = request.form["empid"]

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS employee (
            empid VARCHAR(20) PRIMARY KEY,
            fname VARCHAR(20),
            lname VARCHAR(20),
            pri_skill VARCHAR(20),
            location VARCHAR(20)
        )
        """)

        connection.commit()

        cursor.execute(
            "SELECT * FROM employee WHERE empid=%s",
            (empid,)
        )

        employee = cursor.fetchone()

        connection.close()

        return render_template(
            "index.html",
            employee=employee
        )

    except Exception as e:
        return f"Database Error: {e}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)