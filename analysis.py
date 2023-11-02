import numpy as np
import multiprocessing
import cProfile
import time
import csv


def prepareTrain():
    newTrainData = np.genfromtxt('train.txt', dtype=np.int32, delimiter='|')
    return newTrainData


def prepareTest():
    test = open('test.txt', 'r')
    tData = []
    for line in test:
        tData.append(line.strip().split("|"))
    result = np.zeros((len(tData), 3), dtype=np.int32)

    for i, row in enumerate(tData):
        for j, cell in enumerate(row):
            if cell == 'None':
                tData[i][j] = 0
            else:
                tData[i][j] = int(tData[i][j])
        result[i][0] = tData[i][0]
        result[i][1] = tData[i][1]

    newTestData = np.zeros([len(tData), len(max(tData, key=lambda x: len(x)))], dtype=np.int32)
    for i, j in enumerate(tData):
        newTestData[i][0:len(j)] = j

    return newTestData, result


def calculateRating(training, testing, final):
    sizeTest = len(testing)
    maxUserID = testing[sizeTest - 1][0]
    minUserID = testing[0][0]
    uniqueID = np.array(list(set([row[0] for row in testing])), dtype=np.int32)
    matchingTraining = [rating for rating in training if rating[0] in uniqueID]

    matching_dict = {}
    for rating in matchingTraining:
        key = rating[0]
        if key not in matching_dict:
            matching_dict[key] = []
        matching_dict[key].append(rating[1:])

    for i, music in enumerate(testing):
        if music[0] in matching_dict:
            for rating in matching_dict[music[0]]:
                if rating[0] in music[1:]:
                    final[i][2] += rating[1]
    final = final[np.lexsort((final[:, 2],))]
    final = final[np.lexsort((final[:, 0],))]

    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        field = ['TrackID', 'Predictor']
        writer.writerow(field)
        j = 0
        for row in final:
            if j in (0, 1, 2):
                s = str(row[0]) + "_" + str(row[1])
                writer.writerow([s, 0])
            elif j in (3, 4, 5):
                s = str(row[0]) + "_" + str(row[1])
                writer.writerow([s, 1])
            j = (j + 1) % 6


if __name__ == "__main__":
    start_time = time.perf_counter()
    trainData = prepareTrain()
    testData, finalRating = prepareTest()
    calculateRating(trainData, testData, finalRating)
    end_time = time.perf_counter()
    total_time = end_time - start_time
    print(total_time / 60)
