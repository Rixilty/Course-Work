import random

p = 0
q = 0
n = 0
phi = 0
e = []
d = 0

n_Factors = []
phi_Factors = []

Lock = []
Key = []

def ready():
    Generate_Prime_Numbers()
    Get_Factors()
    Get_e()
    Get_d()
    print(Lock)
    print(Key)
    num = 5
    enc = (num**e)%n
    dec  = (enc**d)%n
    print(num)
    print("Encrypted:",enc)
    print("Decrypted:",dec)

def Generate_Prime_Numbers():
    global p, q, n, phi
    for i in range(2):
        num = random.randint(100, 1000)
        while is_prime(num) == False:
            num = random.randint(100, 1000)
        if p == 0:
            p = num
        else:
            q = num
    p = 2
    q = 7
    n = p * q
    phi = (p - 1) * (q - 1)
    print("p:",p, "q:",q, "n:",n, "phi:",phi)

def is_prime(num):
    if num % 2 == 0 or num <= 1:
        return False
    return True

def Get_Factors():
    for i in range(1, n + 1):
        if n % i == 0 and i != 1:
            n_Factors.append(i)
    for i in range(1, phi + 1):
        if phi % i == 0 and i != 1:
            phi_Factors.append(i)

def Get_e():
    global e, Lock
    for i in range(2, n+1):
        if not is_factor_of_n(i) and not is_factor_of_phi(i):
            e.append(i)
            e = int(e[0])
            Lock = [e, n]
            break

def is_factor_of_n(num):
    for i in range(len(n_Factors)):
        if num % n_Factors[i] == 0 and num != 1:
            return True
    return False

def is_factor_of_phi(num):
    for i in range(len(phi_Factors)):
        if num % phi_Factors[i] == 0 and num != 1:
            return True
    return False

def Get_d():
    global d, Key
    count = 0
    for i in range(n):
        if (i*e)%phi == 1:
            count += 1
            if count == 2:
                d = i
                Key = [d, n]
                break

ready()