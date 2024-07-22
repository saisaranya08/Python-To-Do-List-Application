

from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# File to store tasks
TASKS_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f)

@app.route("/", methods=["GET", "POST"])
def index():
    message = request.args.get("message", "")
    tasks = load_tasks()
    
    if request.method == "POST":
        if "task" in request.form:
            task = request.form.get("task")
            priority = request.form.get("priority").lower()  # Convert priority to lowercase
            tasks.append({"task": task, "priority": priority, "completed": False})
        elif "complete" in request.form:
            task_id = int(request.form.get("task_id"))
            tasks[task_id]["completed"] = True
        elif "submit_tasks" in request.form:
            completed_tasks = [task for task in tasks if task["completed"]]
            with open("submitted_tasks.txt", "w") as f:
                for task in completed_tasks:
                    f.write(f"{task['task']} - {task['priority']} - Completed\n")
            message = "Completed tasks submitted successfully!"
        save_tasks(tasks)
        return redirect(url_for("index", message=message))

    return render_template("index.html", tasks=tasks, message=message)

@app.route("/delete/<int:task_id>")
def delete(task_id):
    tasks = load_tasks()
    tasks.pop(task_id)
    save_tasks(tasks)
    return redirect(url_for("index"))

@app.route("/complete/<int:task_id>", methods=["POST"])
def complete(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks[task_id]["completed"] = True
        save_tasks(tasks)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)





