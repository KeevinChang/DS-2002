import requests
import sqlite3
import time


def make_table():
    conn = sqlite3.connect("requests.db")
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS requests (
                factor INT,
                pi FLOAT,
                time DATETIME
                ); """)
    conn.close()


def get_and_insert():
    response = requests.get("https://4feaquhyai.execute-api.us-east-1.amazonaws.com/api/pi")
    data = response.json()

    conn = sqlite3.connect("requests.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO requests (factor,pi,time) VALUES (?,?,?)",
                (data["factor"], data["pi"], data["time"]))
    conn.commit()
    conn.close()


if __name__=="__main__":
    start_time = time.time()
    duration = 60*60
    make_table()
    while time.time() - start_time < duration:
        get_and_insert()
        time.sleep(60)

    conn = sqlite3.connect("requests.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM requests")
    print(cur.fetchall())
    conn.close()
