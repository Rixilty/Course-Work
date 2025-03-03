import random

p = 0
q = 0
n = 0
phi = 0
e = []
d = 0

Prime_Numbers = []

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


def is_prime(num):
    pass