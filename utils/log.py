from datetime import datetime

def log(string):
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f'{current_datetime}: {string}')
    with open("output.log", "a+") as file:
        print(f'{current_datetime}: {string}', file = file)