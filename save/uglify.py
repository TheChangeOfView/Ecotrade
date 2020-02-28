import json

with open("save/default.json", "r") as file:

    data = json.load(file)

with open("save/default.json", "w") as file:

    json.dump(data, file)