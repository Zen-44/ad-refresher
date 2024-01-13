from datetime import datetime
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "..", "output.log")

def log(string):
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f'{current_datetime}: {string}')
    with open(file_path, "a+") as file:
        print(f'{current_datetime}: {string}', file = file)