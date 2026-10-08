def fib(n:int) -> list[int]:
    fib_list:list[int]= [0,1]
    while fib_list[-1] <= n:
        fib_list.append(fib_list[-1] + fib_list[-2])
    fib_list.remove(fib_list[-1])
    return fib_list

def even_sum(fib_list:list[int]) -> int:
    sum:int = 0
    for n in fib_list:
        if n % 2 == 0:
            sum += n
    return sum

fib_list = fib(4000000)
sum = even_sum(fib_list=fib_list)
print(sum)
