import random
import time

p = 0
q = 0
n = 0
phi = 0
e = []
d = 0

phi_Factors = []

Lock = []
Key = []

Text = []

def ready():
    start_time = time.time()

    Generate_Prime_Numbers()
    Get_Factors()
    Get_e()
    Get_d()
    Message()
    Encrypt(Text)
    Decrypt(Text)

    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Execution Time: {execution_time:.6f} seconds")

def Generate_Prime_Numbers():
    global p, q, n, phi
    for i in range(2):
        num = random.randint(100, 1000)
        while is_prime(num) == False:
            num = random.randint(100, 1000)
        if p == 0:
            p = num
        else:
            while num == p:
                num = random.randint(100, 1000)
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
    for i in range(1, phi + 1):
        if phi % i == 0 and i != 1:
            phi_Factors.append(i)

def Get_e():
    global e, Lock
    for i in range(2, n+1):
        if not is_factor_of_phi(i):
            e.append(i)
            e = int(e[0])
            print("e:",e)
            Lock = [e, n]
            break

def is_factor_of_phi(num):
    for i in range(len(phi_Factors)):
        if num % phi_Factors[i] == 0 and num != 1:
            return True
    return False

def Get_d():
    global d, Key
    for i in range(n ** 2):
        if (i * e) % phi == 1:
            d = i
            Key = [d, n]
            break

def Message():
    Message = "Hello World!!! привет как дела!!! 안녕하세요 مرحبا كيف حالك" #input("Enter a message: ")
    message_to_unicode(Message)

def message_to_unicode(Message):
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