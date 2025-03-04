import random

p = 0
q = 0
n = 0
phi = 0
e = []
d = 0

n_Factors = []
phi_Factors = []

Lock = 0
Key = 0

def Generate_Prime_Numbers():
    global p, q
    for i in range(2):
        num = random.randint(1000, 9999)
        while is_prime(num) == False:
            num = random.randint(1000, 9999)
        if p == 0:
            p = num
        else:
            q = num
    n = p * q
    phi = (p - 1) * (q - 1)
    print("p:",p, "q:",q, "n:",n, "phi:",phi)
    Get_e()


def is_prime(num):
    if num % 2 == 0 or num <= 1:
        return False
    return True


def Get_e():
    for i in range(2, phi+1):
        e.append(i)
    print("e:",e)
    Get_Factors_Of_n()

def Get_Factors_Of_n():
    for i in range(1, n+1):
        if n % i == 0 and i != 1:
            n_Factors.append(i)
    print("n_Factors:",n_Factors)
