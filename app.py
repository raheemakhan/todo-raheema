from flask import Flask, render_template, request, redirect

app = Flask(__name__)
TASKS_FILE = 'tasks.txt'

# Read tasks from file
def load_tasks():
    tasks = []
    try:
        with open(TASKS_FILE, 'r') as file:
            for line in file:
                task, status = line.strip().split('|')
                tasks.append({'task': task, 'done': status == 'done'})
    except FileNotFoundError:
        pass
    return tasks

# Save tasks to file
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        for t in tasks:
            status = 'done' if t['done'] else 'pending'
            file.write(f"{t['task']}|{status}\n")

@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    if task:
        tasks = load_tasks()
        tasks.append({'task': task, 'done': False})
        save_tasks(tasks)
    return redirect('/')

@app.route('/toggle/<int:index>')
def toggle(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks[index]['done'] = not tasks[index]['done']
        save_tasks(tasks)
    return redirect('/')

@app.route('/delete/<int:index>')
def delete(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks.pop(index)
        save_tasks(tasks)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
