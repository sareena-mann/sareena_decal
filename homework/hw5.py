#PART 1

#1 You can use pwd
#2 You can use ls -a
#3 Git pull origin main
#4 mv ~/python_decal/judy_decal/homework.py ~/personal_repo/homework/
#5 cat homework.py
#6 nano homework.py
#7 git add .
#  git commit -m "message"
#  git push origin main
#8 You need to pull changes first before pushing your own.
#9 cd ~/Recents/

#PART 2
def CheckType(value):
    return type(value).__name__

def evenOrOdd(num):
    if (num % 2 == 0):
        return 'even'
    else:
        return 'odd'

#PART 3
def sumWithLoop(list):
    sum = 0;
    for i in list:
        sum += i
    return sum

#PART 4
def duplicateList(list):
    r = []
    for i in list:
        r.append(i)
        r.append(i)
    
    return r

def square(num):
    return num * num



