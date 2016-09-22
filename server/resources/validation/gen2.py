n = 99
m = 9999
alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz"
from random import randrange, choice
def generate():
    return "".join([alpha[randrange(0, len(alpha))] for _ in range(randrange(5, 10))])

frs = {}
for _ in range(n):
    frs[generate()] = randrange(0, 100)

fin = open('resources/inspections/2.in', 'w')
fou = open('resources/inspections/2.out', 'w')

fin.write(str(n) + '\n')
for key, value in frs.items():
    fin.write(key + ' ' + str(value) + '\n')
fin.write(str(m) + '\n')

action = ['a', 'm', 's']
key = list(frs)
for _ in range(m):
    act = randrange(0, 3)
    fin.write(action[act] + ' ')
    if act == 0:
        tar = choice(key)
        fin.write(tar + ' ')
        obj = randrange(-100, 100)
        fin.write(str(obj) + '\n')
        frs[tar] += obj
    elif act == 1:
        tar = choice(key)
        fin.write(tar + ' ')
        obj = randrange(-100, 100)
        fin.write(str(obj) + '\n')
        frs[tar] -= obj
    elif act == 2:
        tar = choice(key)
        fin.write(tar + '\n')
        fou.write(str(frs[tar]) + '\n')
