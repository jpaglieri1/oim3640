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

def get_date_key(keys):
    """Find the date field in keys"""
    for key in keys:
        if 'date' in key.lower():
            return key
    return None

def sort_by_date(items, keys):
    """Sort items by date field, earliest first"""
    date_key = get_date_key(keys)
    if not date_key:
        return items
    return sorted(items, key=lambda x: x.get(date_key, ''))

agendas = load_agendas()

@app.route('/')
def home():
    sorted_agendas = {}
    for name, data in agendas.items():
        # Create sorted items with original index for edit links
        sorted_items = []
        for idx, item in enumerate(data["items"]):
            sorted_items.append({
                "item": item,
                "original_index": idx
            })
        # Sort by date
        date_key = get_date_key(data["keys"])
        if date_key:
            sorted_items.sort(key=lambda x: x["item"].get(date_key, ''))
        
        sorted_agendas[name] = {
            "keys": data["keys"],
            "items": sorted_items,
            "use_dates": data.get("use_dates", True),
            "use_times": data.get("use_times", True)
        }
    return render_template('index.html', agendas=sorted_agendas)

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
            # Store whether to use date/time inputs
            use_dates = request.form.get('include_dates') == '1'
            use_times = request.form.get('include_times') == '1'
            # Add Date/Time fields to keys if checkboxes are checked
            if use_dates and "Date" not in keys and "Due Date" not in keys:
                keys.insert(0, "Date")
            if use_times and "Time" not in keys and "Start Time" not in keys:
                # Find where to insert time field (after date if present)
                insert_idx = 1 if use_dates else 0
                keys.insert(insert_idx, "Start Time")
        else:
            keys = get_keys(format_choice)
            use_dates = True
            use_times = True
        agendas[name] = {"keys": keys, "items": [], "use_dates": use_dates, "use_times": use_times}
        save_agendas(agendas)
        return redirect(url_for('home'))
    return render_template('create.html')

@app.route('/add/<agenda_name>', methods=['GET', 'POST'])
def add_item(agenda_name):
    if agenda_name not in agendas:
        return "Agenda not found", 404
    data = agendas[agenda_name]
    keys = data["keys"]
    use_dates = data.get("use_dates", True)
    use_times = data.get("use_times", True)
    if request.method == 'POST':
        item = {}
        for key in keys:
            item[key] = request.form[key]
        agendas[agenda_name]["items"].append(item)
        save_agendas(agendas)
        return redirect(url_for('home'))
    return render_template('add.html', agenda_name=agenda_name, keys=keys, use_dates=use_dates, use_times=use_times)

@app.route('/view/<agenda_name>')
def view(agenda_name):
    if agenda_name not in agendas:
        return "Agenda not found", 404
    data = agendas[agenda_name]
    # Create sorted items with original index
    sorted_items = []
    for idx, item in enumerate(data["items"]):
        sorted_items.append({
            "item": item,
            "original_index": idx
        })
    # Sort by date
    date_key = get_date_key(data["keys"])
    if date_key:
        sorted_items.sort(key=lambda x: x["item"].get(date_key, ''))
    return render_template('view.html', agenda_name=agenda_name, keys=data["keys"], items=sorted_items)

@app.route('/edit/<agenda_name>/<int:item_index>', methods=['GET', 'POST'])
def edit(agenda_name, item_index):
    if agenda_name not in agendas:
        return "Agenda not found", 404
    data = agendas[agenda_name]
    items = data["items"]
    keys = data["keys"]
    use_dates = data.get("use_dates", True)
    use_times = data.get("use_times", True)
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
    return render_template('edit.html', agenda_name=agenda_name, item_str=item_str, keys=keys, item=item, use_dates=use_dates, use_times=use_times)

@app.route('/delete/<agenda_name>', methods=['POST'])
def delete_agenda(agenda_name):
    if agenda_name not in agendas:
        return "Agenda not found", 404
    del agendas[agenda_name]
    save_agendas(agendas)
    return redirect(url_for('home'))

@app.route('/delete/<agenda_name>/<int:item_index>', methods=['POST'])
def delete_item(agenda_name, item_index):
    if agenda_name not in agendas:
        return "Agenda not found", 404
    items = agendas[agenda_name]["items"]
    if item_index < 0 or item_index >= len(items):
        return "Item not found", 404
    del items[item_index]
    save_agendas(agendas)
    return redirect(url_for('view', agenda_name=agenda_name))

def get_time_key(keys):
    """Find the time field in keys"""
    for key in keys:
        if 'time' in key.lower() and 'start' in key.lower():
            return key
    for key in keys:
        if 'time' in key.lower():
            return key
    return None

def get_date_key(keys):
    """Find the date field in keys"""
    for key in keys:
        if 'date' in key.lower():
            return key
    return None

@app.route('/full')
def full_list():
    all_items = []
    for agenda_name, data in agendas.items():
        keys = data["keys"]
        date_key = get_date_key(keys)
        time_key = get_time_key(keys)
        for item in data["items"]:
            date_val = item.get(date_key, '') if date_key else ''
            time_val = item.get(time_key, '') if time_key else ''
            # Items without time go at the bottom (use 'zzz' as placeholder)
            sort_time = time_val if time_val else 'zzz'
            all_items.append({
                "agenda": agenda_name,
                "keys": keys,
                "item": item,
                "date": date_val,
                "time": time_val,
                "sort_time": sort_time
            })
    # Sort by date, then by time (items without time go to end)
    all_items.sort(key=lambda x: (x["date"], x["sort_time"]))
    return render_template('full.html', items=all_items)

if __name__ == '__main__':
    app.run(debug=True)