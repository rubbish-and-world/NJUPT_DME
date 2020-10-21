import numpy as np

def get_input():
    try:
        elements = input("Enter the elements of set A (saparated with ','): ").split(',')
        l = len(elements)
        m = np.zeros((l,l),dtype=int)
        print(r"Enter the elements of relation R , (in the format of [a,b]\n , end with new line):")
        ls = input().lstrip('[').rstrip(']').split(',')
        while ls != ['']:
            first = elements.index(ls[0])
            second = elements.index(ls[1])
            m[first][second] = 1
            ls = input().lstrip('[').rstrip(']').split(',')
    except:
        print("invalid input")
        exit(0)
    return m

def reflexive(matrix):
    for i in np.diag(matrix):
        if i == 0:
            return False
    return True

def antireflexive(matrix):
    for i in np.diag(matrix):
        if i == 1:
            return False
    return True

def symmetric(matrix):
    return (matrix == np.transpose(matrix)).all()

def antisymmetric(matrix):
    return np.logical_or(np.identity(len(matrix)) , np.logical_xor(matrix , np.transpose(matrix))).all()

def transitive(matrix):
    return (np.logical_or(np.linalg.matrix_power(matrix,2) , matrix) == matrix).all()

matrix = get_input()
print("The attributes ascribed to ralation R : ",end='')
if reflexive(matrix):
    print("reflexive",end=' ')
if antireflexive(matrix):
    print('antireflexive',end=' ')
if symmetric(matrix):
    print('symmetric',end=' ')
if antisymmetric(matrix):
    print('antisymmetric',end=' ')
if transitive(matrix):
    print('transitive')
