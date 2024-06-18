from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/upload', methods=['POST'])
def upload_data():
    value = request.form.get('value')
    if value:
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('INSERT INTO sensor_data (value) VALUES (?)', (value,))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'value': value}), 200
    else:
        return jsonify({'status': 'failure', 'message': 'No value provided'}), 400

@app.route('/data', methods=['GET'])
def get_data():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM sensor_data')
    data = c.fetchall()
    conn.close()
    return jsonify(data), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
