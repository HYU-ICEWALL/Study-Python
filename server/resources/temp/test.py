n = int(input())
q = []
for _ in range(n):
	c = input()
	if c=='get':
		if len(q):
			print(q.pop())
	elif c=='put':
		q.append(int(input()))
print (len(q))