#Q2.1

name = []
for i in range(21):
    name.append(i)


#Q2.2
def squareList(l):
    for index in range(len(l)):
        l[index] = l[index] * l[index]
    return l

anotherNameYouWant = squareList(name)

#2.3
def first_fifteen_elements(g):
    return g[:15]

x = first_fifteen_elements(anotherNameYouWant)
print(x)

#2.4

def every_fifth_element(t):
    x = 4
    retList = []
    while (x < len(t)):
        retList.append(t[x])
        x = x+ 5
    return retList

y = every_fifth_element(anotherNameYouWant)
print(y)

#2.5
def fancy_function(hello):
    hello = hello[:-3]
    hello.reverse()
    return hello

print(fancy_function(x))

#3.1
def create2D():
    array = []
    list = []
    count = 1
    for i in range(5):
        for j in range(5):
            list.append(count)
            count += 1
        array.append(list)
        list = []
    return array

m = create2D()
print(m)


def modify(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] % 3 == 0:
                matrix[i][j] = "?"

    return matrix

print(modify(m))

#3.3
def sum_notQuestion(arr):
    sum = 0
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if arr[i][j] != "?":
                sum += arr[i][j]

    return sum
print(sum_notQuestion(m))