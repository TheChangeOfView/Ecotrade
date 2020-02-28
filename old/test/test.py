import json

items = {"item.name" : "item", "item.buy" : "buy"}
ports = {"port.name" : "port", "port.area" : "area"}

data = {"items.data" : items, "ports.data" : ports}

with open("test.json", "w") as file:
    json.dump(data, file)
    
lol = {}

with open("test.json", "r") as file:
    lol = json.load(file)
    
print (lol)