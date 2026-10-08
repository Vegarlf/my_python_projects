
def palindrome_finder(digit:int) ->dict[str,int]:
    '''
    abcdef = fedcba
    100000a +10000b+1000c+100d+10e+f = 100000f+10000e+1000d+100c+10b+a
    99999a+9990b+900c =FUCK IT
    '''
    min_digit_no:int = (10**(digit))
    max_digit_no:int = (10**(digit+1)) - 1
    palindrome_dict:dict[str,int] = {}
    for x in range(max_digit_no, min_digit_no - 1, -1):
        for y in range(max_digit_no, min_digit_no -1, -1):
            no:int = x*y
            no_rvr:int = int(str(no)[::-1])
            if no == no_rvr:
                palindrome_dict[str(str(x)+'*'+str(y))] = no
    return palindrome_dict
palindrome_dict = palindrome_finder(2)

seen:set[int] = set()
palindrome_dict_clean:dict[str,int] = {}

for k,v in palindrome_dict.items():
    if v not in seen:
        seen.add(v)
        palindrome_dict_clean[k] = v

sorted_palindrome_clean = dict(sorted(palindrome_dict_clean.items(), key = lambda item:item[-1], reverse=True))

print(list(sorted_palindrome_clean.items())[:5])