### Music quiz for OCR GCSE Computer Science (9-1) ###
## Copyright 2020 Liam Staras

# import required libraries
import csv

# read song database from csv
with open('songs.csv') as csvfile:
    songs = list(csv.reader(csvfile))
