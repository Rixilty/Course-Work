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

def ready():
    Generate_Prime_Numbers()
    Get_Factors()
    Get_e()
    Get_d()
    Message()
    Encrypt(Text)
    Decrypt(Text)

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
    n = p * q
    phi = (p - 1) * (q - 1)
    print("p:",p, "q:",q, "n:",n, "phi:",phi)

def is_prime(num):
    for i in range(2, (num//2)):
        if num % i == 0:
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
            print("e:",e)
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
    for i in range(n**2):
        if (i*e)%phi == 1:
            count += 1
            if count == 2:
                d = i
                Key = [d, n]
                break

def Message():
    Message = input("Enter a message: ")
    message_to_ascii(Message)

def message_to_ascii(Message):
    global Text
    for char in Message:
        Text.append(ord(char))

def Encrypt(Text):
    for i in range(len(Text)):
        Text[i] = (Text[i] ** e) % n
    print(Text)

def Decrypt(Text):
    for i in range(len(Text)):
        Text[i] = chr((Text[i] ** d) % n)
    Text = ''.join(Text)
    print(Text)

ready()