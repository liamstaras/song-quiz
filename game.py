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
attempts = 0 # set counter to enter while loop [in another programming language, a REPEAT...UNTIL or equivalent loop would be most appropriate as this would not have to be defined twice]
while not(attempts >= ATTEMPTS): # halt executuion if attemp cap exceeded (2nd test)
    attempts = 0 # reset counter for each new song
    song = random.choice(songs) # select a random song
    print('Guess the song!')
    while not(attempts >= ATTEMPTS): # halt executuion if attemp cap exceeded (1st test)
        if attempts > 0:
            print('try again')
        print('Artist: '+song[1])
        print('Song: '+song[0]) # NEXT: add routine to obliterate part of the name
        guess = input() # NEXT: add case redundancy; FUTURE: add fancy overwriting input?
        if guess == song[0]:
            print('Well done!')
            break # drop out of loop on correct attempt and pick new song
        else:
            attempts += 1 # ONLY increase counter if attempt failed