def isPrime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if not n % i:
            return False
    return True

for i in range(100):
    a = int(input())
    if isPrime(a):
        print ('1')
    else:
        print('0')
