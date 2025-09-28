


mylist = [0,1,2,3,4,5]

print(mylist)

mylist.append(6)

print(mylist)

mylist.extend([55,54,56,78])

print(mylist)

mylist.insert(0,999)

print(mylist)

mylist.remove(55)

print(mylist)

x = mylist.pop(0)

print(x, mylist)

while(len(mylist)):
    x = mylist.pop()
    print(x)

print(mylist)

mylist.extend([55,54,56,78])
mylist.clear()

print(mylist)

mylist = ["pierre","rosalie", "sacha", "andrea"]

mylist.sort()
print(mylist)
mylist.reverse()
print(mylist)

print(mylist.count(0))

print(mylist.index("pierre"))

mylist2 = mylist.copy() 

print(mylist2)

