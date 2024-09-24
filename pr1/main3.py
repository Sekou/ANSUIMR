import itertools
import sys, pygame
import numpy as np
import math

arr=[]
with open("log.txt", "r") as f:
    lines=f.readlines()
    for l in lines:
        tokens=l.split("; ")
        arr.append(tokens)

print(arr)


#TODO: i=argmax(Q:=1/(L+20*N))