def find_all(string, sub):
    start = 0
    while True:
        start = string.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)
for _ in range(int(input())):
    w = input()
    t = input()
    k = sorted(list(find_all(t, ' ' + w + ' ')) + list(find_all(t, ' ' + w)) + list(find_all(t, w + ' ')))
    print ('--'.join(t[:k[0]].split()))
    print ('--'.join(t[k[-1] + len(w) + 1:].split()))