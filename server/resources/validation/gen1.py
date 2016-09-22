from random import randrange
def isPrime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if not n % i:
            return False
    return True

inf = open('resources/inspections/1.in', 'w')
out = open('resources/inspections/1.out', 'w')
 
for i in range(100):
    n = randrange(10, 10000)
    inf.write(str(n) + '\n')
    out.write(isPrime(n) and '1\n' or '0\n')

inf.close()
out.close()

