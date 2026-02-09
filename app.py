from flask import Flask, request, jsonify, send_from_directory
import cx_Oracle
import os

app = Flask(__name__, static_folder='../frontend/assets', template_folder='../frontend')

# Oracle database connection
# cx_Oracle.init_oracle_client(lib_dir=r"C:\oraclexe\instantclient_21_17")  # Commented out to use Oracle Client from system PATH. Ensure it's installed and PATH is set.
dsn = cx_Oracle.makedsn("localhost", 1521, service_name="XE")
connection = cx_Oracle.connect(user="system", password="saran", dsn=dsn)

@app.route('/')
def serve_index():
    return send_from_directory(app.template_folder, 'index.html')

@app.route('/assets/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    print("GET /tasks called")
    try:
        cursor = connection.cursor()
        print(f"Connected to schema: {connection.username}")
        cursor.execute("SELECT * FROM tasks")
        tasks = [
            {
                "id": row[0],
                "description": row[1],
                "start_date": row[2].strftime('%Y-%m-%d') if row[2] else None,
                "end_date": row[3].strftime('%Y-%m-%d') if row[3] else None,
                "priority": row[4],
                "completed": bool(row[5])
            }
            for row in cursor.fetchall()
        ]
        cursor.close()
        return jsonify(tasks)
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"Database error: {error.message}")
        return jsonify({"error": "Database error occurred"}), 500

@app.route('/tasks', methods=['POST'])
def add_task():
    print("POST /tasks called")
    data = request.json
    print(f"Received data: {data}")
    try:
        cursor = connection.cursor()
        task_id_var = cursor.var(cx_Oracle.NUMBER)
        cursor.execute(
            """
            INSERT INTO tasks (description, start_date, end_date, priority, completed)
            VALUES (:1, TO_DATE(:2, 'YYYY-MM-DD'), TO_DATE(:3, 'YYYY-MM-DD'), :4, :5)
            RETURNING id INTO :6
            """,
            (data['description'], data['start_date'], data['end_date'], data['priority'], int(data['completed']), task_id_var)
        )
        task_id = int(task_id_var.getvalue()[0])
        print(f"Inserted task with ID: {task_id}")
        connection.commit()
        cursor.close()
        return jsonify({
            "id": task_id,
            "description": data['description'],
            "start_date": data['start_date'],
            "end_date": data['end_date'],
            "priority": data['priority'],
            "completed": data['completed']
        }), 201
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"Database error: {error.message}")
        return jsonify({"error": "Database error occurred"}), 500

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    print(f"PUT /tasks/{task_id} called")
    data = request.json
    print(f"Received data for update: {data}")
    try:
        required_fields = ['description', 'start_date', 'end_date', 'priority', 'completed']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE tasks
            SET description=:1, start_date=TO_DATE(:2, 'YYYY-MM-DD'), end_date=TO_DATE(:3, 'YYYY-MM-DD'),
                priority=:4, completed=:5
            WHERE id=:6
            """,
            (data['description'], data['start_date'], data['end_date'], data['priority'], int(data['completed']), task_id)
        )
        connection.commit()
        cursor.close()
        return jsonify({"message": "Task updated successfully"})
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"Database error: {error.message}")
        return jsonify({"error": "Database error occurred"}), 500

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    print(f"DELETE /tasks/{task_id} called")
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM tasks WHERE id=:1", (task_id,))
        connection.commit()
        cursor.close()
        return jsonify({"message": "Task deleted successfully"})
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"Database error: {error.message}")
        return jsonify({"error": "Database error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=True)