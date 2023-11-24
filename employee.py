import csv
# import random
import uuid, os
with open('TrimmedData/Team Members.csv') as csvFile:
    Data = csv.reader(csvFile)
    next(Data)
    next(Data)
    next(Data)
    next(Data)
    header = []
    body = []
    i = 0
    for row in Data:
        if i < 12 :
            header.append(row[0].split('\n')[0])
            body.append(row[3])
            i = i+1
        else:
            break

print(header)
print(body)       