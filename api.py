from flask import Flask
import sqlite3

app = Flask(__name__)

connection = sqlite3.connect("db/facts.db", check_same_thread=False)
cursor = connection.cursor()

@app.route("/getrandom")
def return_fact():
    fact = cursor.execute("SELECT fact FROM facts ORDER BY RANDOM() LIMIT 1").fetchall()[0][0]
    return {"response":fact}

if __name__ == "__main__":
    app.run()