from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

def get_keys(format_choice):
    if format_choice == "School":
        return ["Due Date", "Class", "Assignment Name", "% Complete"]
    elif format_choice == "Work":
        return ["Date", "Time", "Task Name", "Location", "% Complete"]
    elif format_choice == "Personal":
        return ["Date", "Start Time", "End Time", "Task Name", "Location", "% Complete"]
    elif format_choice == "Other":
        # For simplicity, assume fixed or handle later
        return ["Task Name", "% Complete"]
    else:
        return []

def load_agendas():
    try:
        with open('agendas.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_agendas(agendas):
    with open('agendas.json', 'w') as f:
        json.dump(agendas, f, indent=4)

agendas = load_agendas()

@app.route('/')
def home():
    return render_template('index.html', agendas=agendas)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        format_choice = request.form['format']
        name = request.form['name']
        if format_choice == "Other":
            columns_str = request.form.get('columns', '').strip()
            if not columns_str:
                # Default or error
                keys = ["Task Name", "% Complete"]
            else:
                keys = [col.strip() for col in columns_str.split(',') if col.strip()]
                if not keys:
                    keys = ["Task Name", "% Complete"]
                if "% Complete" not in keys:
                    keys.append("% Complete")
        else:
            keys = get_keys(format_choice)
        agendas[name] = {"keys": keys, "items": []}
        save_agendas(agendas)
        return redirect(url_for('home'))
    return render_template('create.html')

@app.route('/add/<agenda_name>', methods=['GET', 'POST'])
def add_item(agenda_name):
    if agenda_name not in agendas:
        return "Agenda not found", 404
    keys = agendas[agenda_name]["keys"]
    if request.method == 'POST':
        item = {}
        for key in keys:
            item[key] = request.form[key]
        agendas[agenda_name]["items"].append(item)
        save_agendas(agendas)
        return redirect(url_for('home'))
    return render_template('add.html', agenda_name=agenda_name, keys=keys)

@app.route('/view/<agenda_name>')
def view(agenda_name):
    if agenda_name not in agendas:
        return "Agenda not found", 404
    data = agendas[agenda_name]
    return render_template('view.html', agenda_name=agenda_name, keys=data["keys"], items=data["items"])

@app.route('/edit/<agenda_name>/<int:item_index>', methods=['GET', 'POST'])
def edit(agenda_name, item_index):
    if agenda_name not in agendas:
        return "Agenda not found", 404
    data = agendas[agenda_name]
    items = data["items"]
    keys = data["keys"]
    if item_index < 0 or item_index >= len(items):
        return "Item not found", 404
    item = items[item_index]
    if request.method == 'POST':
        for key in keys:
            item[key] = request.form[key].strip()
        if item.get("% Complete") in ["100", "100%"]:
            del items[item_index]
        save_agendas(agendas)
        return redirect(url_for('home'))
    item_str = ", ".join(f"{k}: {v}" for k, v in item.items())
    return render_template('edit.html', agenda_name=agenda_name, item_str=item_str, keys=keys, item=item)

if __name__ == '__main__':
    app.run(debug=True)