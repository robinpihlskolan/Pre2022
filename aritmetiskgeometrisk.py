#Funktioner för att räkna ut aritmetisk och geometrisk summa


def aritmetisk(start, diff, n):
    summa=0
    for i in range(n):
        next = start+diff*i
        summa=summa+next
    return summa

def geometrisk(start, mult, n):
    summa=0
    for i in range(n):
        next = start*mult**i
        summa=summa+next
    return summa

try:
    file = open("Myfile1.txt", "w")
    file.write(str(aritmetisk(3,2,4)))
    file.close()
except IOError:
    msg = ("Unable to create file on disk.")
    file.close()

print(aritmetisk(3,2,4))
print(geometrisk(3,2,4))


