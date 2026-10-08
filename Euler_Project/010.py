import numpy as np
import time
from functools import wraps
import math
#2,000,000
DEBUG:bool=True
#!all_no = np.arange(2,2000001, dtype=int)
#print(all_no)
#!prime_list:list[int] = [0]
#while prime_list[-1] <= 2000000:
#    for x in all_no:
#        prime_list.append(int(x))
#        if DEBUG:
#            print(f"checked {x}, {x in prime_list}")
#    all_no = all_no[all_no%prime_list[-1] == 0]
i = 0

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.perf_counter() - start:.4f}s")
        return result
    return wrapper

@timer
def prime_list_maker(tilln:int, *, debug:bool = False):
    all_no = np.arange(2,tilln+1, dtype=int)
    prime_list:list[int] = [0]
    while prime_list[-1] <= math.isqrt(tilln) + 1 :
        temp = all_no[0]
        prime_list.append(int(temp))
        if DEBUG:
            print(f"added {int(temp)}")
        all_no = all_no[all_no%temp != 0]
        if DEBUG:
            print(f"all_no len = {len(all_no)}")
    prime_to_add = all_no.tolist()
    prime_list.extend(prime_to_add)
    return prime_list

prime_list = prime_list_maker(2000000, debug = True)
print(prime_list)
print(len(prime_list))
print(f"sum is {sum(prime_list)}")


