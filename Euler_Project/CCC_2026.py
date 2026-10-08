#J1
B = 5
T = 100
P = 70

left = T - P
if B > left:
    print("N")
else:
    left_2 = left -B
    print(f"Y {left_2}")
