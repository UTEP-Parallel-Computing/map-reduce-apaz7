#Alejandro Paz
#Map Reduce Lab
import pymp
import re
import time

def count_words(files, word_list, total):
    f = open(files, 'r')
    for i in word_list:
        total[i] += len(re.findall(i, f.read().lower()))
        f.seek(0)

def reducing(files, word_list, cores):

    total = pymp.shared.dict()

    with pymp.Parallel(cores) as p:

        for i in word_list:
            total[i] = 0

        lock = p.lock

        for j in p.iterate(files):
            lock.acquire()
            count_words(j, word_list, total)
            lock.release()

    print(total)


files = ["shakespeare1.txt", "shakespeare2.txt", "shakespeare3.txt", "shakespeare4.txt", 
        "shakespeare5.txt", "shakespeare6.txt", "shakespeare7.txt", "shakespeare8.txt"]
word_list = ["hate", "love", "death", "night", "sleep", "time", "henry", "hamlet", 
            "you", "my", "blood", "poison", "macbeth", "king", "heart", "honest"]
cores = [1,2,4,8]

for i in range(len(cores)):
    start = time.time()
    reducing(files, word_list, cores[i])
    end = time.time()
    print("Total time with ", cores[i], " cores: ", end - start)
