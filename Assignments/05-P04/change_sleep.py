import json
from random import randint

for k in range(5):
    with open(f"instructions/program_{k}.exe") as file:
        data = json.load(file)

    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j].split(" ")[0] == "sleep":
                x = randint(5, 15)
                data[i][j] = f"sleep {x}"
        
    with open(f"instructions/program_{k}.exe", 'w') as file:
        json.dump(data, file, indent=3)

