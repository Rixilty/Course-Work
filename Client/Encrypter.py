import random
import time

prime_p = 0
prime_q = 0
modulus_n = 0
phi = 0
public_exponent = []
private_exponent = 0

phi_Factors = []

Lock = []
Key = []

Text = []

def ready():
    start_time = time.time()

    Generate_Prime_Numbers()
    Get_Factors()
    Get_public_exponent()
    Get_private_exponent()
    Message()
    Encrypt(Text)
    Decrypt(Text)

    print("Public key:", Lock)
    print("Private key:", Key)

    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Execution Time: {execution_time:.6f} seconds")

def Generate_Prime_Numbers():
    global prime_p, prime_q, modulus_n, phi
    for i in range(2):
        num = random.randint(100, 1000)
        while is_prime(num) == False:
            num = random.randint(100, 1000)
        if prime_p == 0:
            prime_p = num
        else:
            while num == prime_p:
                num = random.randint(100, 1000)
            prime_q = num
    modulus_n = prime_p * prime_q
    phi = (prime_p - 1) * (prime_q - 1)
    print("p:",prime_p, "q:",prime_q, "n:",modulus_n, "phi:",phi)

def is_prime(num):
    for i in range(2, (num//2)):
        if num % i == 0:
            return False
    return True

def Get_Factors():
    for i in range(1, phi + 1):
        if phi % i == 0 and i != 1:
            phi_Factors.append(i)

def Get_public_exponent():
    global public_exponent, Lock
    for i in range(2, modulus_n+1):
        if not is_factor_of_phi(i):
            public_exponent.append(i)
            public_exponent = int(public_exponent[0])
            print("public_exponent:",public_exponent)
            Lock = [public_exponent, modulus_n]
            break

def is_factor_of_phi(num):
    for i in range(len(phi_Factors)):
        if num % phi_Factors[i] == 0 and num != 1:
            return True
    return False

def Get_private_exponent():
    global private_exponent, Key
    for i in range(modulus_n):
        if (i * public_exponent) % phi == 1:
            private_exponent = i
            Key = [private_exponent, modulus_n]
            break

def Message():
    Message = "Hello World!!! привет как дела!!! 안녕하세요 مرحبا كيف حالك"#input("Enter a message: ")
    message_to_unicode(Message)

def message_to_unicode(Message):
    global Text
    for char in Message:
        Text.append(ord(char))
    print(Text)

def Encrypt(Text):
    for i in range(len(Text)):
        Text[i] = pow(Text[i], public_exponent, modulus_n)
    print(Text)

def Decrypt(Text):
    for i in range(len(Text)):
        Text[i] = chr(pow(Text[i], private_exponent, modulus_n))
    Text = ''.join(Text)
    print(Text)

ready()