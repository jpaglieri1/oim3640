def formats():
    formatops = ["School", "Work", "Personal", "Other"]
    while True:
        print("Available formats:", formatops)
        agendaopt = input("Input format choice: ").strip()
        if agendaopt == "School":
            keys = ["Due Date", "Class", "Assignment Name", "% Complete"]
            return keys
        elif agendaopt == "Work":
            keys = ["Date", "Time", "Task Name", "Location", "% Complete"]
            return keys
        elif agendaopt == "Personal":
            keys = ["Date", "Start Time", "End Time", "Task Name", "Location", "% Complete"]
            return keys
        elif agendaopt == "Other":
            try:
                cols = int(input("Input number of columns: ").strip())
                keys = []
                for i in range(cols):
                    colname = input(f"Input column name {i+1}: ").strip()
                    keys.append(colname)
                return keys
            except ValueError:
                print("Invalid number")
                continue
        else:
            print("Invalid input, try again")

def calcreate(agendalist):
    keys = formats()
    dict_name = input("Insert agenda name: ").strip()
    agendalist[dict_name] = {"keys": keys, "items": []}
    print(f"Agenda '{dict_name}' created.")
    return agendalist

def add_item(agendalist):
    if not agendalist:
        print("No agendas available.")
        return
    print("Available agendas:")
    for name in agendalist:
        print(f"- {name}")
    name = input("Choose agenda name: ").strip()
    if name not in agendalist:
        print("Agenda not found.")
        return
    item = {}
    for key in agendalist[name]["keys"]:
        item[key] = input(f"{key}: ").strip()
    agendalist[name]["items"].append(item)
    print("Item added.")

def view_agenda(agendalist):
    if not agendalist:
        print("No agendas available.")
        return
    print("Available agendas:")
    for name in agendalist:
        print(f"- {name}")
    name = input("Choose agenda name to view: ").strip()
    if name not in agendalist:
        print("Agenda not found.")
        return
    items = agendalist[name]["items"]
    keys = agendalist[name]["keys"]
    if not items:
        print("No items in this agenda.")
        return
    print(f"\nAgenda: {name}")
    print("-" * 50)
    # Print header
    header = " | ".join(f"{key:<15}" for key in keys)
    print(header)
    print("-" * len(header))
    for item in items:
        row = " | ".join(f"{item.get(key, ''):<15}" for key in keys)
        print(row)
    print()

def edit_completion(agendalist):
    if not agendalist:
        print("No agendas available.")
        return
    print("Available agendas:")
    for name in agendalist:
        print(f"- {name}")
    name = input("Choose agenda name: ").strip()
    if name not in agendalist:
        print("Agenda not found.")
        return
    items = agendalist[name]["items"]
    if not items:
        print("No items in this agenda.")
        return
    print("Items:")
    for i, item in enumerate(items):
        print(f"{i}: {item}")
    try:
        idx = int(input("Choose item index to edit % Complete: ").strip())
        if idx < 0 or idx >= len(items):
            print("Invalid index.")
            return
        if "% Complete" not in items[idx]:
            print("This agenda does not have % Complete field.")
            return
        new_complete = input("New % Complete: ").strip()
        items[idx]["% Complete"] = new_complete
        print("Updated.")
    except ValueError:
        print("Invalid input.")

def homescreen(agendalist):
    print("\n" + "="*50)
    print("AGENDA MANAGER")
    print("="*50)
    if not agendalist:
        print("No agendas currently active.")
    else:
        print("Active agendas:")
        for agenda_name in agendalist:
            print(f"\nAgenda: {agenda_name}")
            items = agendalist[agenda_name]["items"]
            if not items:
                print("  (No items)")
            else:
                for item in items:
                    # Print item as key: value pairs
                    item_str = ", ".join(f"{key}: {value}" for key, value in item.items())
                    print(f"  - {item_str}")
    print("\nOptions:")
    print(" 1. Create New Agenda")
    print(" 2. View Agenda")
    print(" 3. Add Item to Agenda")
    print(" 4. Edit % Complete")
    print(" 5. Exit")
    while True:
        try:
            choice = int(input("Insert action by corresponding number: ").strip())
            if 1 <= choice <= 5:
                return choice
            else:
                print("Invalid choice, enter 1-5.")
        except ValueError:
            print("Invalid input, enter a number.")

# Main application
agendas = {}
while True:
    choice = homescreen(agendas)
    if choice == 1:
        calcreate(agendas)
    elif choice == 2:
        view_agenda(agendas)
    elif choice == 3:
        add_item(agendas)
    elif choice == 4:
        edit_completion(agendas)
    elif choice == 5:
        print("Exiting...")
        break