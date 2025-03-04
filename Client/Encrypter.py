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

def ready():
    Generate_Prime_Numbers()
    Get_e()
    Get_Factors_Of_n()
    Get_Factors_Of_phi()
    Get_Non_Coprime_Numbers()

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

def is_prime(num):
    if num % 2 == 0 or num <= 1:
        return False
    return True

def Get_e():
    for i in range(2, phi+1):
        e.append(i)
    print("e:",e)

def Get_Factors_Of_n():
    for i in range(1, n+1):
        if n % i == 0 and i != 1:
            n_Factors.append(i)
    print("n_Factors:",n_Factors)

def Get_Factors_Of_phi():
    for i in range(1, phi+1):
        if phi%i == 0 and i != 1:
            phi_Factors.append(i)
    print("phi_Factors:",phi_Factors)

def Get_Non_Coprime_Numbers():
    for i in range(len(e)):
       for j in range(len(n_Factors)):
          if e[i] % n_Factors[j] == 0:
              e.remove(e[i])
       for j in range(len(phi_Factors)):
           if e[i] % phi_Factors[j] == 0:
               e.remove(e[i])
    print("e:",e)

ready()