import pymp
import re

files = ["shakespeare1.txt", "shakespeare2.txt", "shakespeare3.txt", "shakespeare4.txt", 
        "shakespeare5.txt", "shakespeare6.txt", "shakespeare7.txt", "shakespeare8.txt"]

words = ["hate", "love", "death", "night", "sleep", "time", "henry", 
        "hamlet", "you", "my", "blood", "poison", "macbeth", "king",
        "heart", "honest"]

def loading_files(text_files):
    with open(text_files) as file:
        combined_files = file.read().lower()
    return combined_files

def count_words(text_files, words):
    print('')
