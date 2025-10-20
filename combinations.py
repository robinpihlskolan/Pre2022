#Make a list of lists with all combinations of numbers
num_letters_in_message = int(input("Number of letters in message: "))
alphabet_size = int(input("Size of the alphabet: "))


def overflow(n, overflownum):
    if n+1>overflownum:
        return True
    else:
        return False

class All_Combos:
    def __init__(self, n, alfabet):
        self.n = n
        self.alfabet = alfabet
        self.combos = [[0]*n]

    def addCombo(self, combo):
        self.combos.append(combo)

    def plusOne(self, currentlist):
        templist = currentlist
        current_position = 0
        while current_position < self.n:
            new_num_in_pos = templist[current_position]+1
            if overflow(new_num_in_pos, self.alfabet):
                new_num_in_pos = 0
                templist[current_position]=new_num_in_pos
                current_position+=1
            else:
                templist[current_position]+=1
                break
        print(templist)
        return templist

    def generate(self):
        current_list = self.combos[-1].copy()
        next_list = self.plusOne(current_list)
        self.addCombo(next_list)


        while next_list!=[alphabet_size-1]*num_letters_in_message:
            current_list = self.combos[-1].copy()
            next_list = self.plusOne(current_list)
            self.addCombo(next_list)
            print(self.combos)
        

    def printlists(self):
        print(self.combos)

combos = All_Combos(num_letters_in_message, alphabet_size)
combos.generate()
combos.printlists()
                
                
        
        
    
