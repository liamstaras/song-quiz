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

# check file prescence
if not os.path.exists('users.csv'):
    print('Warning! - no users database found. Creating...')
    with open('users.csv','w') as csvfile:
        csv.writer(csvfile).writerow(['username','hash','salt','score'])


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
## authentication subsystem
print('Please provide credentials.')
# read all users from csv
with open('users.csv') as csvfile:
    users = list(csv.reader(csvfile))[1:] # read all users into a list of lists [Python equiv. of array]
username = input('Username: ') # prompt for the username
foundUser = False # we are looping through all users in a linear search; we need to know if we found anything afterwards
for user in users:
    if user[0] == username: # comparing each row from the csv
        foundUser = True # make note if the user is found
        break # we don't need to check any more users if one is found
if foundUser: # in this case, the user already exists
    while True: # we'll just keep going indefinitely here - who would brute-force a command line song quiz anyway? [and the spec. does not tell us to have resilience to this sort of attack]
        password = input('Password: ') # ask the user for their password
        salt = bytes.fromhex(user[2]) # get the salt from the database
        hash = hashlib.pbkdf2_hmac('sha256',password.encode('utf-8'),salt,100000) # generate a hash from the password and salt using 100,000 iterations of SHA256
        if hash.hex() == user[1]: # if the generated hash is the same as the stored hash, the password was correct
            bestScore = int(user[3]) # store the user's best score information
            break # if the password was correct, we're done and the user is authenticated
        else:
            print('Incorrect password.')
else: # otherwise, we create a new user
    print('User not found; creating new user.')
    password = input('Password: ') # ask the user for a password
    salt = os.urandom(32) # create a "random" salt
    hash = hashlib.pbkdf2_hmac('sha256',password.encode('utf-8'),salt,100000) # generate a hash from the password and salt using 100,000 iterations of SHA256
    with open('users.csv','a') as csvfile: # open the user database in append mode
        csv.writer(csvfile).writerow([username,hash.hex(),salt.hex(),0]) # write one row to the end of the csv with the username, the hex of the hash and salt, and a best score of 0
del(password) # delete the password variable - get it out of RAM!
del(user) # we don't need this any more
del(users) # same here

# at this point, we have the variable 'username' as the username of the authenticated user and we can begin the game
# we also have 'bestScore' as the top score for the authenticated user

## game routine
attempts = 0 # set counter to enter while loop [in another programming language, a REPEAT...UNTIL or equivalent loop would be most appropriate as this would not have to be defined twice]
score = 0 # counter for the user's score
while not(attempts >= ATTEMPTS): # halt executuion if attempt cap exceeded (2nd test)
    attempts = 0 # reset counter for each new song
    song = random.choice(songs) # select a random song
    print() # a blank line
    print('Guess the song!')
    blankName = firstLetter(song[0]) # blank out part of the name of the song
    while not(attempts >= ATTEMPTS): # halt executuion if attempt cap exceeded (1st test)
        print() # a blank line
        print('Score: '+str(score)+'; High Score: '+str(bestScore))
        print('Attempt '+str(attempts+1)+'/'+str(ATTEMPTS))
        if attempts > 0:
            print('Try again.') # if the user has still got attempts left, this will be shown
        print('Artist: '+song[1])
        print('Song: '+blankName) # display a blanked out song name
        guess = input() # FUTURE: add fancy overwriting input?
        if guess.lower() == song[0].lower():
            print('Well done!')
            break # drop out of loop on correct attempt and pick new song
        else:
            print('Incorrect.')
            attempts += 1 # ONLY increase counter if attempt failed
    score += 1+ATTEMPTS-attempts # the score is increased by the number of attempts the user had remainaing

# at this point, the game is finished
print('Game over!')
print('You scored: '+str(score))
if score > bestScore:
    print('New high score!!')
    bestScore = score

## write the new best to the database and display all-time high scores
# read in all users
with open('users.csv') as csvfile:
    users = list(csv.reader(csvfile))
# locate and update the user in the array
for user in users[1:]:
    if user[0] == username: # comparing each row from the csv
        user[3] = bestScore # update the best score in the array
        break # we don't need to check any more users if one is found
# write the array back to the file
with open('users.csv','w') as csvfile:
    csv.writer(csvfile).writerows(users)

# find maximum scores
print('HIGH SCORES')
scorers = [[int(user[3]),user[0]] for user in users[1:]] # get all scores in to a list
for idx, scorer in enumerate(sorted(scorers,reverse=True)[:5]): # sort the list and select the first five elements
    print(str(idx+1)+'. '+str(scorer[1])+': '+str(scorer[0])) # display the name and score