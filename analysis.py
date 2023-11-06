import numpy as np
import multiprocessing
import cProfile
import time
import csv


def prepareTrain():
    # save training data as a np array
    newTrainData = np.genfromtxt('train.txt', dtype=np.int32, delimiter='|')
    return newTrainData


def prepareTest():
    test = open('test.txt', 'r')
    tData = []
    # split test line by line with delimeter
    for line in test:
        tData.append(line.strip().split("|"))
    result = []

    # convert Nones into 0, strings into int, and append user id, item d, 0 rating, and blank list (for genre stats)
    # to final result list
    for i, row in enumerate(tData):
        for j, cell in enumerate(row):
            if cell == 'None':
                tData[i][j] = 0
            else:
                tData[i][j] = int(tData[i][j])
        row = [tData[i][0], tData[i][1], 0, 0, 0, []]
        result.append(row)

    # convert testing array into a np array
    newTestData = np.zeros([len(tData), len(max(tData, key=lambda x: len(x)))], dtype=np.int32)
    for i, j in enumerate(tData):
        newTestData[i][0:len(j)] = j

    return newTestData, result


def calculateRating(training, testing, final):
    # match IDs from testing array to training, so we don't iterate over unnecessary data
    uniqueID = np.array(list(set([row[0] for row in testing])), dtype=np.int32)
    matchingTraining = [rating for rating in training if rating[0] in uniqueID]

    # create a dict of all ratings per user
    matching_dict = {}
    for rating in matchingTraining:
        key = rating[0]
        if key not in matching_dict:
            matching_dict[key] = []
        matching_dict[key].append(rating[1:])

    # find matching user IDs from testing in training dict
    # for every rating [] for the selected user, check if the rating is a song, artist, or album id -
    # if so add rating to final rating
    # if the rating is a genre, add the value to genre [] for later calculations
    for i, music in enumerate(testing):
        if music[0] in matching_dict:
            for rating in matching_dict[music[0]]:
                if rating[0] == music[1]:
                    final[i][2] += rating[1]
                if rating[0] == music[2]:
                    final[i][3] += rating[1]
                if rating[0] == music[3]:
                    final[i][4] += rating[1]
                if rating[0] in music[4:]:
                    final[i][5].append(rating[1])


    # calculate stats for genre data
    for i, row in enumerate(final):
        genreCount = len(row[5])
        # if we had genre ratings, find max, min, sum, avg, and var
        if genreCount > 0:
            maxScore = max(row[5])
            minScore = min(row[5])
            sumScore = sum(row[5])
            averageScore = np.average(row[5])
            varianceScore = np.var(row[5])
            mean_rating = np.mean(row[5])
            std_deviation = np.std(row[5])
            # METHOD 1 - SIMPLE AVERAGE, SCORE=.85
            #final[i][2] += averageScore
            # METHOD 2 - ADD ALL STATS, SCORE=.77
            #final[i][2] = final[i][2] + maxScore + minScore + sumScore + averageScore + varianceScore'
            # METHOD 3 - ADD SUM OF SCORES, SCORE=.84
            #final[i][2] += sumScore
            # METHOD 4 - WEIGHT GENRE LOWER, WEIGHT SONG/ARTIST/ALBUM HIGHER, THEN ADD, SCORE=.86
            #song_artist_album = 9 * final[i][2]
            #genre = 1 * sumScore
            #overall = (song_artist_album + genre) / (9+1)
            #final[i][2] = 0
            #inal[i][2] += overall
        # METHOD 5 - WEIGHT SONG, ALBUM, ARTIST, THEN GENRE, SCORE=
            genreW = sumScore * 1
        else:
            genreW = 0
        songW = final[i][2] * 9
        albumW = final[i][3] * 5
        artistW = final[i][4] * 3
        overall = (songW + artistW + albumW + genreW) / (9 + 5 + 3 + 1)
        final[i][2] = 0
        final[i][2] = overall
        # delete the genre calculation row, we don't need it anymore
        del final[i][5], final[i][4], final[i][3]


    # sort final calculations by rating
    # sort final calculations by user ID, so the final array is sorted by rating per user
    # first 3 tracks are lowest scores, next 3 tracks are highest scores
    # this makes writing to csv easier
    final = np.array(final, dtype=np.int32)
    final = final[np.lexsort((final[:, 2],))]
    final = final[np.lexsort((final[:, 0],))]

    # write to csv
    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        # add header
        field = ['TrackID', 'Predictor']
        writer.writerow(field)
        j = 0
        for row in final:
            # if row = 1-3, predictor is 0
            if j in (0, 1, 2):
                s = str(row[0]) + "_" + str(row[1])
                writer.writerow([s, 0])
            # ir row = 3-6, predictor is 1
            elif j in (3, 4, 5):
                s = str(row[0]) + "_" + str(row[1])
                writer.writerow([s, 1])
            # reset or iterate j
            j = (j + 1) % 6


if __name__ == "__main__":
    # calculate time to process all of the data modeling
    start_time = time.perf_counter()
    trainData = prepareTrain()
    testData, finalRating = prepareTest()
    calculateRating(trainData, testData, finalRating)
    end_time = time.perf_counter()
    total_time = end_time - start_time
    print(total_time / 60)

# to do
# parallel processing for input read
# add genre stats to final result, get some kind of calculation from it
# make testing list dict instead
