#!/usr/bin/python3
import random
alphabets=[]

alpha = 'a'
for i in range(0, 26):
    alphabets.append(alpha)
    alpha = chr(ord(alpha) + 1)

def cipher(file_name):
    numbers=[]
    new = []
    a=len(file_name)
    for i in range(0,a):
        numbers.append(random.randint(97,123))
    for i in range(0,a):
        sub=(abs(ord(file_name[i]) - numbers[i]))
        new.append(chr(97 + sub))

    no_space=''
    return (no_space.join(new))
