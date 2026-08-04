from flask import Flask, render_template, request
import pymysql
import os
from config import *

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"

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
            location VARCHAR(20),
            document_path VARCHAR(255)
        )
        """)

        connection.commit()

        cursor.execute("SELECT * FROM employee WHERE empid=%s", (empid,))
        employee = cursor.fetchone()

        connection.close()

        return render_template("index.html", employee=employee)

    except Exception as e:
        return f"Database Error: {e}"

@app.route("/updateemployee", methods=["POST"])
def update_employee():
    empid = request.form["empid"]
    fname = request.form["firstname"]
    lname = request.form["lastname"]
    pri_skill = request.form["skills"]
    location = request.form["location"]
    file = request.files.get("document")

    document_path = None

    if file and file.filename:
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        document_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(document_path)

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE employee
            SET fname=%s,
                lname=%s,
                pri_skill=%s,
                location=%s,
                document_path=%s
            WHERE empid=%s
        """, (fname, lname, pri_skill, location, document_path, empid))

        connection.commit()
        connection.close()

        return "Employee updated successfully"

    except Exception as e:
        return f"Database Error: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)