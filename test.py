from random import shuffle


def f():    
    testList = []
    for i in range(1, 101):
        testList.append(i)

    shuffle(testList)
    return testList

l = f()
print(l)

li = []
li = f()
print(li)