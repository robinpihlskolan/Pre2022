inlist = [[[1,2],[3,4]],[5,6,7],[8,9]]

def flatten(mylist):
    if mylist == []:
        return mylist
    if isinstance(mylist[0], list):
        return flatten(mylist[0])+ flatten(mylist[1:])
    return mylist[:1] + flatten(mylist[1:])

print(flatten(inlist))
