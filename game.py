#### Music quiz for OCR GCSE Computer Science (9-1) ####
### Copyright 2020 Liam Staras ###

## initialization
# import required libraries
import csv
import random
import os
import hashlib

# define constants
ATTEMPTS = 2 # how many guesses the user gets for each song
BLANKING = None # what to replace removed characters with in the name

## functions
# firstLetter function - get the first letter of each word
def firstLetter(phrase, fill=BLANKING):
    if fill == None:
        fill = ''
    return ' '.join([word[0] + fill*(len(word)-1) for word in phrase.split(' ')])

# read song database from csv
with open('songs.csv') as csvfile:
    songs = list(csv.reader(csvfile))[1:] # actually read in the songs, skip header row

## main program
# authentication subsystem
print('Please provide credentials.')
with open('users.csv') as csvfile:
    users = list(csv.reader(csvfile))[1:]
username = input('Username: ')
foundUser = False
for user in users:
    if user[0] == username:
        foundUser = True
        break
if foundUser: # in this case, the user already exists
    while True:
        password = input('Password: ')
        salt = bytes.fromhex(user[2])
        hash = hashlib.pbkdf2_hmac('sha256',password.encode('utf-8'),salt,100000)
        if hash.hex() == user[1]:
            break
        else:
            print('Incorrect password.')
else: # otherwise, we create a new user
    print('User not found; creating new user.')
    password = input('Password: ')
    salt = os.urandom(32)
    hash = hashlib.pbkdf2_hmac('sha256',password.encode('utf-8'),salt,100000)
    with open('users.csv','a') as csvfile:
        csv.writer(csvfile).writerow([username,hash.hex(),salt.hex(),0])
del(password)


# game routine
attempts = 0 # set counter to enter while loop [in another programming language, a REPEAT...UNTIL or equivalent loop would be most appropriate as this would not have to be defined twice]
while not(attempts >= ATTEMPTS): # halt executuion if attemp cap exceeded (2nd test)
    attempts = 0 # reset counter for each new song
    song = random.choice(songs) # select a random song
    print('Guess the song!')
    blankName = firstLetter(song[0]) # blank out part of the name of the song
    while not(attempts >= ATTEMPTS): # halt executuion if attemp cap exceeded (1st test)
        if attempts > 0:
            print('Try again.')
        print('Artist: '+song[1])
        print('Song: '+blankName) # display a blanked out song name
        guess = input() # FUTURE: add fancy overwriting input?
        if guess.lower() == song[0].lower():
            print('Well done!')
            break # drop out of loop on correct attempt and pick new song
        else:
            attempts += 1 # ONLY increase counter if attempt failed