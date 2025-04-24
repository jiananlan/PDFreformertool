import math

for i in range(10000):
    f = 2 ** (i**3) + (2**i) ** 2
    g = i ** (i**2) + i**5
    print(f < g)
