import random
import json
data = {}
getname=['A', 'B', 'C']


for i in range(3):
    name = getname[i]
    temp={}
    for j in range(100, 255, 5):
        temp[j]=random.randrange(1, 10)
    data[name]=temp
        

with open('memory.json', 'w') as f:
    json.dump(data, f, indent=4)


    