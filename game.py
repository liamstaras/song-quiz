### Music quiz for OCR GCSE Computer Science (9-1) ###
## Copyright 2020 Liam Staras

# import required libraries
import csv
import random

# define constants
ATTEMPTS = 2

# read song database from csv
with open('songs.csv') as csvfile:
    songs = list(csv.reader(csvfile))[1:] # actually read in the songs, skip header row

# game routine
attempts = 0
while not(attempts >= ATTEMPTS):
    attempts = 0
    song = random.choice(songs)
    print('Guess the song!')
    while not(attempts >= ATTEMPTS):
        if attempts > 0:
            print('try again')
        print('Artist: '+song[1])
        print('Song: '+song[0])
        guess = input()
        if guess == song[0]:
            print('Well done!')
            break
        else:
            attempts += 1