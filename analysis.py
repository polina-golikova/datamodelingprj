import pandas as pd
import numpy as np
output_file = 'myOutput.txt'

fOut = open(output_file, 'w')
test = open('testTrack_hierarchy.txt', 'r')
train = open('trainIdx2_matrix.txt', 'r')

testData = []
trainData = []

for line in test:
    testData.append(line.strip().split("|"))
for line in train:
    trainData.append(line.strip().split("|"))

result = []
for i, row in enumerate(testData):
    for j, cell in enumerate(row):
        if cell == 'None':
            testData[i][j] = 0
        else:
            testData[i][j] = int(testData[i][j])
    result.append([testData[i][0], testData[i][1], 0])
    
for i, row in enumerate(trainData):
    for j, cell in enumerate(row):
        trainData[i][j] = int(trainData[i][j])            


for i, row in enumerate(trainData):
    for j, music in enumerate(testData):
        if trainData[i][0] == testData[j][0]:
            if trainData[i][1] in testData[j][1:]:
                result[j][2] += trainData[i][2]
                break

for row in result:
    print(result)
    
for i, row in enumerate(result):
    outStr = ""
    outStr += str(result[i][0]) + "|" + str(result[i][1]) + "|" + str(result[i][2])
    fOut.write(outStr + '\n')

fOut.close()
