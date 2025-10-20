kombinationer = []

antal_platser = int(input("Platser: "))
antal_nummer = int(input("Vad för Max tal: "))

nummerin = (antal_nummer + 1)

for _ in range(nummerin**antal_platser):
    kombination = []
    for plats in range(antal_platser):
        kombination.append(_ // (nummerin**plats) % nummerin)
    kombinationer.append(kombination)

print(kombinationer)
