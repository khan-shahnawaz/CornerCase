import random
tests=random.randint(1,100)
print(tests)
for test in range(tests):
    n=random.randint(1,10)
    l=[random.randint(1,20) for i in range(n)]
    print(n)
    print(*l)
