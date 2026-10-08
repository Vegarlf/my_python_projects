#10001
from math import isqrt
def prime_check(n:int):
    for x in range(2, isqrt(n) + 1):
        if n % x == 0:
            return False
    return True
def prime_list(tilln:int):
    plist:list[int] = []
    x:int = 2
    while len(plist) < tilln:
        if prime_check(x):
            plist.append(x)
        x+=1
    return sorted(plist)

return_list = prime_list(10001)
print(return_list, len(return_list))
print(return_list[-1])
