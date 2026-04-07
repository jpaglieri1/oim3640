def formats():
    formatops = ["School", "Work", "Personal", "Other"]
    agendaopt = input("Input format choice: ")
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
        cols = input("Input number of columns: ")
        keys = []
        for i in range(cols):
            colname = input("Input column name: ")
            keys.append(colname)
        return keys
    else:
        print("Invalid input")

def calcreate(keys, agendalist):
    dict_name = input("Insert calendar name: ")
    agendalist[dict_name] = dict.fromkeys(formats())
    return agendalist
    
def homescreen(agendalist):
    if len(agendas) == 0:
        print("No agendas currently active\n")
    else:
        for agenda in range(agendalist):
            print(agenda)
            print("\n")
    print ("Options:")
    print(" 1. Create New Agenda\n 2. Add item to Agenda\n 3. Edit completion")
    choice = int(input("Insert action by corresponding number: "))
    return choice

agendas = []
homescreen(agendas)