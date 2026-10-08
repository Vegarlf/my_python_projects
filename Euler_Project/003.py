#600851475143

def max_factorisatuon(n:int) -> int:
    factors:list[int] = []
    d:int = 2
    while d*d <= n:
        while n%d==0:
            factors.append(d)
            n //=d
        d+=1
    if n >=1:
        factors.append(n)
    return max(factors)

print(max_factorisatuon(600851475143))
