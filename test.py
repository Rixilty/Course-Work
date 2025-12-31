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

Text = []

#O(1)

def ready(): #O(n^2)
    Generate_Prime_Numbers()
    Get_Factors()
    Get_e()
    Get_d()
    Message()
    Encrypt(Text)
    Decrypt(Text)

def Generate_Prime_Numbers():
    global p, q, n, phi
    for i in range(2): #O(2) --> O(1)
        num = random.randint(1000, 9999) #O(1)
        while is_prime(num) == False: #O(9) * O(n/2) --> O(n)
            num = random.randint(1000, 9999) #O(1)
        if p == 0:
            p = num #O(1)
        else:
            while num == p: #O(1)
                num = random.randint(1000, 9999) #O(1)
            q = num #O(1)
    n = p * q #O(1)
    phi = (p - 1) * (q - 1) #O(1)
    print("p:",p, "q:",q, "n:",n, "phi:",phi) #O(1)

def is_prime(num):
    for i in range(2, (num//2)): #O(n/2)
        if num % i == 0:
            return False
    return True

def Get_Factors():
    for i in range(1, n + 1):
        if n % i == 0 and i != 1: #O(n)
            n_Factors.append(i)
    for i in range(1, phi + 1): #O(phi)
        if phi % i == 0 and i != 1:
            phi_Factors.append(i)

def Get_e():
    global e, Lock
    for i in range(2, n+1): #O(n)
        if not is_factor_of_n(i) and not is_factor_of_phi(i): #O(√n+√phi) ≈ O(√n)
            e.append(i)
            e = int(e[0])
            print("e:",e)
            Lock = [e, n]
            break

def is_factor_of_n(num):
    for i in range(len(n_Factors)): #O(√n)
        if num % n_Factors[i] == 0 and num != 1:
            return True
    return False

def is_factor_of_phi(num):
    for i in range(len(phi_Factors)): #O(√phi)
        if num % phi_Factors[i] == 0 and num != 1:
            return True
    return False

def Get_d():
    global d, Key
    count = 0
    for i in range(n**2): #O(n^2)
        if (i*e)%phi == 1:
            count += 1
            if count == 2:
                d = i
                Key = [d, n]
                break

def Message():
    Message = input("Enter a message: ")
    message_to_ascii(Message) #O(Message)

def message_to_ascii(Message):
    global Text
    for char in Message: #O(Message)
        Text.append(ord(char))

def Encrypt(Text):
    for i in range(len(Text)): #O(Message)
        Text[i] = (Text[i] ** e) % n #O(log(Message))
    print(Text)

def Decrypt(Text):
    for i in range(len(Text)):#O(Message)
        Text[i] = chr((Text[i] ** d) % n)#O(log(Message))
    Text = ''.join(Text) #O(1)
    print(Text) #O(1)

ready()