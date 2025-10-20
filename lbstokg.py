# lbs to kg or kg to lbs

while True:
    try:
        print("0: lbs to kg")
        print("1: kg to lbs")
        mode = int(input())
        if not(mode==0 or mode==1):
            raise ValueError  #Ge ett värdefel om mode inte är noll eller ett
        else:
            break
    except ValueError: #Hantera värdefelet
        print("Only 0 or 1 are valid inputs")

while True:
    try:
        print("Enter value: ")
        value = int(input())
        if not value>=0:
            raise ValueError #Ge ett värdefel om value inte är positivt
        else:
            break
    except ValueError: #Hantera värdefelet
        print("Not a valid value. Only positive integers are accepted.")

if mode==0:
    kg=value*0.45359237
    print(str(value)+" lbs = "+str(kg)+" kg" )
else:
    lbs=value*2.20462262
    print(str(value)+" kg = "+str(lbs)+" lbs" )
    
