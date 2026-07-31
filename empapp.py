from flask import Flask
import pymysql
from config import *

app = Flask(__name__)

@app.route('/')
def home():
    try:
        connection = pymysql.connect(
            host=customhost,
            user=customuser,
            password=custompass,
            database=customdb,
            port=customport
        )

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

        cursor.execute("SELECT COUNT(*) FROM employee")
        count = cursor.fetchone()[0]

        connection.close()

        return f"""
        <h1>AWS RDS Connected Successfully</h1>
        <p>Total Employees: {count}</p>
        """

    except Exception as e:
        return f"Database Error: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)