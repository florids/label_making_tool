import json
a = "yangfan"
b = '123'
with open(r"user.json","r") as f:
    data = json.load(f)
for i in range(len(data)):
    if a in data[i]['account'] and b == data[i]['password']:
        print("succeess")

