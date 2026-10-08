# a+b+c=1000
# a^2 +b^2 = c^2
# a<b<c
import time
DEBUG:bool=True
answer=[]
flag:bool = False
start = time.perf_counter()
for a in range(1,999 + 1):
    for x in range(1, 999 + 1):
        if a+x >999:
            continue
        b = a+x
        if a**2 + b**2 == (1000 - (a+b))**2:
            flag = True
            answer.append(a)
            answer.append(b)
            if DEBUG:
                print(f"checked{a},{b} : {flag}")
        else:
            flag = False
            if DEBUG:
                print(f"checked{a},{b} : {flag}")
end = time.perf_counter()
print(f"took {end-start:.4f} seconds")
print(answer)
c = 1000-(answer[0] + answer[1])
print(f"{a},{b},{c} = {answer[0]}, {answer[1]}, {c}")
prod=answer[0]*answer[1]*c
print(f"product is {prod}")