from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQLdb
from flask import Flask, request, jsonify
from flask_cors import CORS  # Optional, allows requests from other apps
import MySQLdb



app = Flask(__name__)
CORS(app)

# ✅ Create DB connection
db = MySQLdb.connect(
    host="localhost",
    user="root",
    password="sathish_0506",  # replace with your password
    database="task_manager"
)


# ✅ POST /tasks — for adding a new task
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    if not title:
        return jsonify({'error': 'Title is required'}), 400

    cursor = db.cursor()
    cursor.execute("INSERT INTO tasks (title, description) VALUES (%s, %s)", (title, description))
    db.commit()
    cursor.close()

    return jsonify({'message': 'Task added successfully'}), 201



# ✅ GET /tasks — for retrieving tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    cursor = db.cursor()
    cursor.execute("SELECT id, title, description, status, created_at FROM tasks")
    rows = cursor.fetchall()
    cursor.close()

    tasks = []
    for row in rows:
        task = {
            'id': row[0],
            'title': row[1],
            'description': row[2],
            'status': row[3],
            'created_at': str(row[4])
        }
        tasks.append(task)

    return jsonify(tasks)

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    status = data.get('status')

    cursor = db.cursor()

    # ✅ Fetch existing title and description
    cursor.execute("SELECT title, description FROM tasks WHERE id = %s", (task_id,))
    task = cursor.fetchone()

    if not task:
        return jsonify({'error': 'Task not found'}), 404

    title, description = task  # Unpack existing data

    cursor.execute("""
        UPDATE tasks
        SET title = %s, description = %s, status = %s
        WHERE id = %s
    """, (title, description, status, task_id))
    db.commit()
    return jsonify({'message': 'Task updated'})


# ✅ Delete a Task by ID
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    db.commit()
    cursor.close()

    return jsonify({'message': 'Task deleted successfully'})


@app.route('/')
def home():
    return render_template('index.html')  # this line is key

