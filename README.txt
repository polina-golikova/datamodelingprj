Importing Data
- training and test data are read into either a numpy array or normal py array
- each file has delimiter (|) and the data is converted into an 32bit int
- final result file is generated using testing data, where each row adds user id, song id, and a rating of "0"

Analysis
- training data is further processed by truncating to only include unique user ids from matching ids in testing data
- a training dict then is generated using user id as a key, and item ids with ratings as nested lists as values to improve run time of operations
- testing data is converted into numpy array to improve run time of operations
- by finding testing user id in the training dict, the code locates if rating in dict matches either song, artist, or album id, where from then that rating is added to initial 0 rating value
- if the found rating is a genre related rating, it is added to a genre rating list that will be later analyzed

Genre Analysis
- for every found genre related rating, we collect count of ratings, max, min, sum, average, variance, mean, and std
- different methods were tested of final rating numbers:
            METHOD 1 - SIMPLE AVERAGE, SCORE=.85
            METHOD 2 - ADD ALL STATS, SCORE=.77
            METHOD 3 - ADD SUM OF SCORES, SCORE=.84
- in the end for this development iteration, we used simple average as it produced the best score on Kaggle
- to improve speed, these genre rating were afterwards deleted

Final Output
- final rating array with sum of ratings was sorted by rating->user id
- results were written to csv (assuming each user had 6 and only 6 songs attributed to them)
- since the results were sorted, first 3 ratings are lowest (0) and last 3 ratings are highest (1)
- these results, along with userid_songid were output to csv

Future Improvements
- current processing speed is 6.5min, this could be improved with full use of dict, less array copy operations, and use of parallel processing py lib.
- we can also improve our scores by using different statistical rating methods