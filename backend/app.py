from flask import Flask, jsonify, request
import mysql.connector
import os

app = Flask(__name__)

db = mysql.connector.connect(
    host=os.environ.get("MYSQL_HOST", "mysql-db"),
    user="root",
    password=os.environ.get("MYSQL_ROOT_PASSWORD", "root123"),
    database="testdb"
)

cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS messages (id INT AUTO_INCREMENT PRIMARY KEY, msg VARCHAR(255))")
db.commit()

@app.route("/add", methods=["POST"])
def add_message():
    msg = request.json.get("msg")
    cursor.execute("INSERT INTO messages (msg) VALUES (%s)", (msg,))
    db.commit()
    return jsonify({"status": "success"}), 201

@app.route("/messages", methods=["GET"])
def get_messages():
    cursor.execute("SELECT * FROM messages")
    result = [{"id": row[0], "msg": row[1]} for row in cursor.fetchall()]
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

