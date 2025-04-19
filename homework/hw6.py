import numpy as np
from sympy import *

#1

def containsPrimes(arr):
    result = []
    for row in arr:
        if any(isprime(x) for x in row):
            result.append(row)
    return np.array(result)

#2
def checkerboard1():
    return np.zeros(8, 8)

def checkerboard2():
    result = np.zeros(8, 8)
    index = 0
    row = 0

    while (row < 8):
        while (index < 8):
            result[row][index] = 1
            index += 2
        row += 2
        index = 0
    
    return result

def checkerboard3():
    arr = checkerboard2()
    last = arr[-1:]
    arr[1:,:]
    arr[0, :] = last
    return arr

def expansion(arr, space):
    return np.array([(" " * n).join(word) for word in arr])

def SecondDimmest(stars):
    arr = np.rot90(stars)
    arr1 = []
    for row in arr:
        row.sort()
        arr2.appen(arr[1])
    return arr1


