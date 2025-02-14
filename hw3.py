#Q1
def computePower(x, y):
    r = x
    for i in range(y-1):
        r = r *x
    return r

print(computePower(2, 3))


#Q2
def temperatureRange(readings):
    return (min(readings), max(readings))

temperatureRange([15, 14, 17, 20, 23, 28, 20])

#Q3
def isWeekend(day):
    return day==6 or day==7

isWeekend(6)

#Q4
def fuel_efficiency(d, f):
    return d/f

fuel_efficiency(70, 21.5)

#Q5
def decodeNumbers(x):
    if (x < 10):
        return str(x)
    
    y = str(x % 10)
    z = str(x // 10)
    return y + z

decodeNumbers(12345)

#Q6.1
def find_min_with_while_loops(ls):
    min = ls[0]
    i = 0;
    while (i < len(ls) -1 ):
        if (ls[i] < min):
            min = ls[i]
        i+=1
    return min

def find_max_with_for_loops(ls):
    max = ls[0]
    for i in ls:
        if (i > max):
            max = i
    return max

find_min_with_while_loops([2024, 98, 131, 2, 3, 72])
find_max_with_for_loops([2024, 98, 131, 2, 3, 72])

#Q7
def vowel_and_consonant_count(s):
    v = 0
    vowels = ["a", "e", "i", "o", "u", "A", "E", "I", "O", "U"]
    cl = []
    vl =[]
  
    for i in s:
        if i in vowels and i.upper() not in vl and i.lower() not in vl :
            vl.append(i)
        elif (i.isalpha() and  i.upper() not in cl and i.lower() not in cl):
            cl.append(i)

    return (len(vl), len(cl))


vowel_and_consonant_count("UC Berkeley, founded in 1868!")

#Q8
def digit_root(n):
    sum = n % 10
    n = n // 10
    while n > 0:
        sum += n % 10
        n = n //10
    return sum

digit_root(2468)
    

print(computePower(2, 3))  # Expected output: 9
print(temperatureRange([15, 14, 17, 20, 23, 28, 20]))  # Expected: (14, 28)
print(isWeekend(6))  # Expected: True
print(fuel_efficiency(70, 21.5))  # Expected: 70 / 21.5
print(decodeNumbers(12345))  # Expected: "54321"
print(find_min_with_while_loops([2024, 98, 131, 2, 3, 72]))  # Expected: 2
print(find_max_with_for_loops([2024, 98, 131, 2, 3, 72]))  # Expected: 2024
print(vowel_and_consonant_count("UC Berkeley, founded in 1868!"))  # Expected: (9, 11)
print(digit_root(2468))  # Expected: 2+4+6+8 = 20
