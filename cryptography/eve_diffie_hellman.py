# Antonia Ritter and McKenna Wirth
# CS338 Spring 2022
# Being Eve Assignment 
# Diffie Hellman 

g = 11
p = 59
A = 57   # A = 11^X mod 59
B = 44   # B = 11^Y mod 59
X = 0
Y = 0
unsolved = True 

# Mystery: X, Y < p
# Secret = B^X mod p = A^Y mod p 
# Looking for X, Y that solve this, X, Y < p

i = 1
j = 1
while unsolved and i<p:
    while unsolved and j<p:
        if (B**i % p) == (A**j % p):
            unsolved = False 
            X = i
            Y = j 
        j+=1
    j = 1
    i+=1


if unsolved:
    print("Unsolved :(")
else:
    print("X = %d, Y = %d" % (X, Y))
    secret = B**X % p
    secret2 = A**Y % p 
    if secret != secret2:   # error-checking 
        print("Something went wrong :(")
    else:
        print("Secret =", secret)