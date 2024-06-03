####################################################################
# ST1507 DSAA: MorseCode Message Analyzer (Morse Class)            #
#------------------------------------------------------------------#
#                                                                  #
# - Name: Aw Shao Yang                                             #
# - Class: DAAA/FT/2B/03                                           #
# - Admission Number: p2012126                                     #
####################################################################


#Node for sorted linked list Classes
class Node:
    def __init__(self):
        self.__nextNode = None

    def get_nextNode(self): 
        return self.__nextNode

    def set_nextNode(self, next_node):
        self.__nextNode = next_node

#Coordinate Class Meant for comparing letter placements
class Coordinate:

    #Ony private attributes users can only set the values when initializing object
    def __init__(self, row, column):
        self.__row = row          #Row of item
        self.__column = column    #Column of item

    #Less than comparison
    def __lt__(self, other_coord):

        #If the row is lesser 
        if self.__row < other_coord.__row:
            return True 

        #If the row is the same but column is lesser
        if self.__column < other_coord.__column and self.__row == other_coord.__row:
            return True 
        else:
            return False

    #Greater than comparison
    def __gt__(self, other_coord):

        #If the row is lesser 
        if self.__row > other_coord.__row:
            return True 

        #If the row is the same but column is lesser
        if self.__column > other_coord.__column and self.__row == other_coord.__row:
            return True 
        else:
            return False

    def __str__(self):
        return f'Coordinate({self.__row},{self.__column})'


#Word object meant for easy word sorting
class Word(Node):

    #Attributes are all privatized so that people cannot set them by themselves, 
    #Values are set only when inserted
    def __init__(self, word=None, placement=[]):
        self.__word = word                    #Associated word
        self.__frequency = len(placement)     #Word frequency is deduced from placement list
        self.__length = len(word)             #Word length is length of word
        self.__placement = placement          #Word coordinates
        super().__init__()              

    #Greater than comparison for word
    def __gt__(self, otherword):

        #If word is more frequent, if equal then if word is shorter, if both equal then alphabets are earlier
        if self.__frequency > otherword.__frequency:
            return True

        elif self.__length < otherword.__length and self.__frequency == otherword.__frequency:
            return True

        elif self.__word < otherword.__word and self.__frequency == otherword.__frequency and self.__length == otherword.__length:
            return True
        else:
            return False 

    #Lesser than comparison for word
    def __lt__(self, otherword):

        #If word is less frequent, if equal then if word is longer, if both equal then alphabets are later
        if self.__frequency < otherword.__frequency:
            return True

        elif self.__length > otherword.__length and self.__frequency == otherword.__frequency:
            return True

        elif self.__word > otherword.__word and self.__frequency == otherword.__frequency and self.__length == otherword.__length:
            return True
        else:
            return False 

    #Print word e.g [HELLO] (6) [(1,2), (2,3), (4,4)]
    def __str__(self):
        return f"[{self.__word}] ({self.__frequency}) {self.__placement}"

    def __repr__(self):
        return repr((self.__word, self.__frequency, self.__length))

    #Convertion of word to Coordinate word
    def word_to_coordword(self):
        return Coordinate_Word(self.__word, self.__placement) 
    
    #getters for subclasses and MorseTool 
    def get_frequency(self):
        return self.__frequency

    def get_placement(self):
        return self.__placement
    
    def get_word(self):
        return self.__word


#Coordinate Word is meant for easy word sorting in WordSorter 
#Sort based on frequency and 1st coordinate in placement [] list 
class Coordinate_Word(Word):

    def __gt__(self, otherword):
        #If frequency is higher and if equal, word appears earlier
        if self.get_frequency() > otherword.get_frequency():
            return True
        if Coordinate(self.get_placement()[0][0], self.get_placement()[0][1]) < Coordinate(otherword.get_placement()[0][0], otherword.get_placement()[0][1]) and self.get_frequency() == otherword.get_frequency():
            return True
        else: 
            return False

    def __lt__(self, otherword):
        #If frequency is lower and if equal, word appears later
        if self.get_frequency < otherword.get_frequency():
            return True
        if Coordinate(self.get_placement()[0][0], self.get_placement()[0][1]) > Coordinate(otherword.get_placement()[0][0], otherword.get__placement()[0][1]) and self.get_frequency() == otherword.get_frequency():
            return True
        else: 
            return False


#Linked List meant for sorting words upon insert 
class WordSorter:
    #Values are privatized as they should'nt be set from outside and sorted only upon insert
    def __init__(self):
        self.__headWord = None
        self.__length = 0

    #Add as the head of the list 
    def __appendToHead(self, newWord):
        oldHeadWord = self.__headWord
        self.__headWord = newWord
        self.__headWord.set_nextNode(oldHeadWord)
        self.__length += 1 

    #Insertion of new items will be sorted as follows 
    def insert(self, newWord):
        self.__length += 1 
        # If list is currently empty the first node is the new node
        if self.__headWord == None:
            self.__headWord = newWord 
            return

        #If the new node is higher than head, assign it
        if newWord > self.__headWord:
            self.__appendToHead(newWord) 
            return

        # Check it is going to be inserted between any pair of Nodes (left,right)
        leftWord = self.__headWord  
        rightWord = self.__headWord.get_nextNode() 
        
        #While the list has not reached the end
        while rightWord != None:

            #If the new node is less than the right node do reassignment
            if newWord > rightWord:
                leftWord.set_nextNode(newWord)
                newWord.set_nextNode(rightWord)
                return

            #If it is still more than the right node move down the list
            leftWord = rightWord
            rightWord = rightWord.get_nextNode()
        
        #If last, then just add to tail
        leftWord.set_nextNode(newWord)
        
    def __str__(self):
    # We start at the head
        output =""
        node= self.__headWord
        firstWord = True
        while node != None:
            if firstWord:
                output = "<" + node.__str__()
                firstWord = False
            else:
                output += (',' + node.__str__())
            node= node.get_nextNode()
        return output + ">"


    #Meant for conversion of sorted linked list to normal py list, with sublists based on frequency
    def node_to_list(self):
        word_list = []
        node = self.__headWord
        while node != None:
            word_list.append(node)
            node = node.get_nextNode()
        #Keeps only unique frequency values

        data = list(set([data.get_frequency() for data in word_list]))

        #Sort the frequencies
        getLength = sorted(data, reverse=True)
        result = []

        #For each frequency
        for length in getLength:

            #Create a list of elements with the same frequency
            frequency_groups = [data for data in word_list if length == data.get_frequency()]
            result.append(frequency_groups)

        return result


#Testing Ground
if __name__ == "__main__":
    pass

