#Alejandro Paz
#To run you have to do mpirun -n <# of threads> python3 map_reduce_MPI.py
import time
import re
from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank() 

def count_words(files, word_list,total):  
    f = open(files, 'r')  
    for w in word_list:  
        total[w] += len(re.findall(w, f.read().lower()))
        f.seek(0)  

def reducing(files, word_list): 

    rank = comm.Get_rank()  
    if rank == 0:
        dict_words = {}
        for word in word_list:
            dict_words[word] = 0  
        if size > 2: 
            for i in range(1, size):
                comm.send(dict_words, dest = i)
    else:
        dict_words = {}
        dict_words = comm.recv(source = 0,)  

    threaded = int(8 / size)  
    slice = threaded * rank  
    limit = int(threaded * (rank + 1))
  
    for j in range(slice, limit):  
        count_words(files[j], word_list, dict_words) 

    if rank != 0:  
        comm.send(dict_words, dest=0, )

    if rank == 0:  
        result = dict_words
        if size > 1:
            for i in range(1, size):
                data = comm.recv(source=i,)
                for k, v in data.items():
                    if k not in result:
                        result[k] = v
                    else:
                        result[k] += v

        return result

files = ["shakespeare1.txt", "shakespeare2.txt", "shakespeare3.txt", "shakespeare4.txt",
             "shakespeare5.txt", "shakespeare6.txt", "shakespeare7.txt", "shakespeare8.txt"]  
word_list = ["hate", "love", "death", "night", "sleep", "time", "henry", "hamlet",  
             "you", "my", "blood", "poison", "macbeth", "king", "heart", "honest"]

start = time.time()
result  = reducing(files, word_list)
end = time.time()


print(result)
print("Total time: ", end - start)