"""Detta program ska lösa ett kryptokorsord.
Alltså ett korsord där varje ruta innehåller en siffra och varje siffra
står för en viss bokstav.
"""





"""---------------------------------------------------------------------
"""




"""
Klasser för en siffer-bokstav kombinationer kallad matchningar
"""
#En enkel bindning av siffra->bokstav
class Single_Match:
    def __init__(self, number, letter):
        self.number = number
        self.letter = letter

    # implements self==other
    def __eq__(self, other): 
        if not isinstance(other, Single_Match):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.number == other.number and self.letter == other.letter


#Lista av bindningar (vilket motsvarar en enskild lösning till kryptokorsordet
class Matches:
    def __init__(self):
        self.list = []

    def add(self, newmatch):
        if len(newmatch.letter)>1:
            print("Okänt fel, bokstav är flera tecken långt.")
        self.list.append(newmatch)

    def existLetter(self, letter):
        for match in self.list:
            if match.letter == letter:
                return True
        return False

    def existNumber(self, number):
        for match in self.list:
            if match.number == number:
                return True
        return False

    def getMatchNumber(self, letter):
        ans = -1
        for match in self.list:
            if match.letter == letter:
                return match.number
        return ans
    
    def getMatchLetter(self, number):
        ans = ""
        for match in self.list:
            if match.number == number:
                return match.letter
        return ans
        

    def print(self):
        for match in self.list:
            print(str(match.number)+"->"+str(match.letter))

#Lista av lösningar till kryptokorsordet
class Matches_List:
    def __init__(self):
        self.list = []

    def add(self, newmatches):
        self.list.append(newmatches)

    def print(self):
        if len(self.list)==0:
            print("Empty")
        for matches in self.list:
            print(" ")
            matches.print()


"""
Word match
"""
#Returnerar True ifall ett ord passar in på kryptokorsordsmönstret annars False
def isAMatch(cryptoword, word): 
    tempmatch = Matches()
    #Se först så att krypto-ordet och ordet är lika långa
    if len(cryptoword) == len(word):
        #Gå igenom varje siffra/bokstavs-par i krypto-ordet
        for i in range(len(cryptoword)):
            current_num = cryptoword[i]
            current_let = word[i]
            #Ifall siffran inte finns, försöka lägga den i tempmatch
            if tempmatch.existNumber(current_num) == False:
                singlematch = Single_Match(current_num, current_let)
                #Dubbelkolla så att bokstaven inte redan tillhör en annan siffra
                if tempmatch.existLetter(current_let):
                    return (False, tempmatch)
                #Returnerades inte False är det okej
                #att lägga till den nya matchningen    
                tempmatch.add(singlematch)
            #Ifall siffran finns men pekar på en annan bokstav, returnera False
            if tempmatch.existNumber(current_num) and not tempmatch.getMatchLetter(current_num)==current_let:
                return (False, tempmatch)

        #Hela listan har traverserats utan problem
        return (True, tempmatch)
            
    else:
        return (False, tempmatch)


def isAMatchWithEarlierMatch(cryptoword, word, match):
    tempmatch = Matches()
    #Kopiera tidigare matchningar till tempmatch
    for m in match.list:
        tempmatch.add(Single_Match(m.number, m.letter))
    #Se först så att krypto-ordet och ordet är lika långa
    if len(cryptoword) == len(word):
        #Gå igenom varje siffra/bokstavs-par i krypto-ordet
        for i in range(len(cryptoword)):
            current_num = cryptoword[i]
            current_let = word[i]
            #Ifall siffran inte finns, lägg den i tempmatch
            if tempmatch.existNumber(current_num) == False:
                singlematch = Single_Match(current_num, current_let)
                tempmatch.add(singlematch)
            #Ifall siffran finns men pekar på en annan bokstav, returnera False
            if tempmatch.existNumber(current_num) and not tempmatch.getMatchLetter(current_num)==current_let:
                return (False, tempmatch)

        #Hela listan har traverserats utan problem
        return (True, tempmatch)
            
    else:
        return (False, tempmatch)


           
    
    


#Gör en initial lista av siffer/bokstavs-matchningar utan att titta på tidigare matchningar 
#med hjälp av det första kryptoordet och ordlistan
def makeAFirstMatch(cryptoword, wordlist):
    result = Matches_List()
    for word in wordlist:
        if len(word)==len(cryptoword):
            temp_result = Matches()
            if isAMatch(cryptoword, word)[0]:
                #Ifall kryptoordet matchar med ordet i ordlistan skapa
                #en matchning av de siffror och bokstäver som hör ihop
                temp_result = isAMatch(cryptoword, word)[1]
                result.add(temp_result)
                
    return result




#Gör en lista av matchningar som utgår från tidigare matchningar och ett krypto-ord
def developMatches(cryptoword, wordlist, cryptomatches):
    result = Matches_List()  # Börja med en tom lista av matchningar

    # Med hjälp av kryptoordet, ordlistan och tidigare matchningar
    # Utveckla eller kasta tidigare matchningar
    for match in cryptomatches.list:
        # Kopiera matchningen för att hantera flera möjliga matchningar
        tempMatch = Matches()
        for m in match.list:
            tempMatch.add(Single_Match(m.number, m.letter))

        # Utveckla matchningen med det nya kryptoordet
        (isValid, updatedMatch) = isAMatchWithEarlierMatch(cryptoword, wordlist, tempMatch)
        
        # Ifall matchningen är giltig, lägg till den i resultatet
        if isValid:
            result.add(updatedMatch)

    # Returnera resultatet av alla matchutvecklingar
    return result
            
        
        

        
           



def solveCrypto(cryptowords, wordlist):

    #1 Börja med en tom lista av matchningar
    matchningar = Matches_List() 
       
    #2. Gå igenom varje kryptoord ett i taget    
    for cryptoword_num in range(len(cryptowords)): #Välj ett nytt kryptoord
        #Ifall det är första kryptoordet
        #skapa första listan av giltiga matchningar
        if cryptoword_num == 0:
            
            
            matchningar=makeAFirstMatch(cryptowords[0], wordlist)
            
        #Ifall det inte är första kryptoordet
        #utveckla matchningarna med nuvarandra kryptoord och tidigare matchningar, 
        #eller kasta matchningar som inte längre är giltiga    
        else:
            
            matchningar=developMatches(cryptowords[cryptoword_num], wordlist, matchningar)
    
    #3. Gör om steg 2 tills du gått igenom alla kryptoord. Gå därefter till steg 4.
    
    #4. Returnera giltiga matchningar.
    return matchningar


ordlista = ["ALL", "TALL", "LAT", "MAT"]

crypto=[]
stop=False
#Här lägger användaren in alla krypto-ord i listan crypto
print("Fyll i ett ord från kryptokorsordet")
print("ex: 1 2 1:")
while not stop:
    a = [int(x) for x in input().split()]
    if a == [0]:
        stop = True
    else:
        crypto.append(a)
        print("Skriv nästa ord eller avsluta med 0 [ENTER]")

solutions = solveCrypto(crypto, ordlista)
if len(solutions.list)==0:
    print("Inga lösningar hittades")
else:
    print("Giltiga lösningar: ")
    solutions.print()

    


