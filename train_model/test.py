import os

url = os.path.join("pos.txt")
with open(url, encoding="utf-8") as file:
    data = file.readlines()

print( data )