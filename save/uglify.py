import json

with open("save/default.eco", "r") as file:

    data = json.load(file)

with open("save/default.eco", "w") as file:

    json.dump(data, file)