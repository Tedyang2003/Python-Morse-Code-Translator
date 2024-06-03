####################################################################
# ST1507 DSAA: MorseCode Message Analyzer (Morse Class)            #
#------------------------------------------------------------------#
#                                                                  #
# - Name: Aw Shao Yang                                             #
# - Class: DAAA/FT/2B/03                                           #
# - Admission Number: p2012126                                     #
####################################################################

import os 
import os.path
current_dir = os.path.dirname(os.path.abspath(__file__))
from WordSorter import Word
from WordSorter import WordSorter

#General morse class
class Morse:
    #Morse Codes transaltion sheet
    __codes = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----'}
    
    #Only morse symbols that are allowed 
    __valid_morse = [',', ' ', '\n', '.', '-']

    #When class is initiated, save message for encoding and a message for decoding 
    def __init__(self,  stop_words_path=None, letter_message=None, morse_message = None, write_file = None):
        
        #Message to encode
        self.letter_message = letter_message    

        #File path to write to 
        if write_file != None:
            if  write_file[-4:] != '.txt':
                raise ValueError('File is invalid or not set. Please set a proper .txt file using set_write_file()')
            else:
                self.__write_file = write_file    
        else:
            self.__write_file = None        

        #Contains a message to be decoded
        if morse_message != None:                 

            for letter in morse_message:
                #Check if txt file only contains allowed data '.'  ','  '-'  '\n'  and  'space'
                if letter not in self.__valid_morse:
                    raise ValueError("Invalid Values. Please have only '.' ',' '\\n' and ' ' in your message ")
        self.__morse_message = morse_message     

        #Stop words file path or list 
        #List for custom quick stop words        
        #Ensure all lowercase 
        if stop_words_path == None:
            self.__stop_words = None

        elif isinstance(stop_words_path, list):
            self.__stop_words = list(map(lambda x: x.lower(), stop_words_path))

        #Accepts a file of stop-words
        elif not os.path.isfile(stop_words_path):
            raise FileNotFoundError("Please enter a valid path or input a custom python list")

        #Stop words from a file
        else:
            with open(current_dir+'\\'+ stop_words_path, 'r') as f:
                lines = f.read()
            self.__stop_words = list(map(lambda x: x.lower(), lines.split('\n')))  



    #Encoder for a full message 
    def encodeMorse(self):
        encoded = ""
        if self.letter_message == None:
            raise  ValueError('Object letter message to be encoded not found use set_letter_message method')
    
        #For each word in the sentence
        for i, item in enumerate(self.letter_message.split(' ')):
            #For each letter in the word
            for letter in item.upper():

                if letter.isalnum() and letter in self.__codes.keys():
                    encoded += self.__codes[letter] + ","
                else: 
                    encoded += letter
                    
            if i != len(self.letter_message.split(' '))-1:
                encoded += ' '
        #Return encoded message 
        return encoded.rstrip(',').lstrip(',')


    #Morse code decoder
    def decodeMorse(self):
        decoded = ""
        #If morse message does not exist
        if self.__morse_message == None:
            raise ValueError('Object morse_message to be decoded not found use set_morse_message() method')

        message = self.__morse_message.split('\n')
        
        for line in range(len(message)):
            #Split into word
            for word in message[line].split(' '):
                #Remove trailing comma
                for letter in list(filter(None,word.split(','))):

                    for key, value in Morse.__codes.items():
                        if letter == value:
                            decoded += key
                        
                decoded += " "
            
            #Check if the line is less than message length to add '\n'
            if line < len(message)-1:
                decoded += '\n'

        return decoded


    #Message analyzer method
    def analyze(self):
        final_message = ""
        print('\n>>> Analysis and sorting has started'+'\n')

        #Decode of morse code
        final_message +='*** Decoded Morse Text\n' 
        decoded_message = self.decodeMorse()
        final_message += decoded_message +'\n\n'
        
        #Returns unique set of words
        unique = Morse.get_unique(decoded_message)

        #Create a word sorter list and locate each words coordinates and insert to WordSorter() as Word() object
        sort_list = WordSorter()
        for item in unique:
            coordinates = Morse.get_coordinates(item, decoded_message)
            word = Word(item, coordinates)
            sort_list.insert(word)

        #Convert sort_list to an actual list() of Word() objects with their frequencies in sublists
        sort_list = sort_list.node_to_list()

        #In each frequency group
        for frequency_grp in sort_list:
            final_message += f'*** Morse Words with frequency=> {frequency_grp[0].get_frequency()}\n'

            #For each word in each frequency group
            for word in frequency_grp:

                #Focus on the word and encode that word
                self.letter_message= word.get_word()
                final_message += self.encodeMorse().rstrip(',').lstrip(',')+ "\n"
                final_message += str(word) + '\n'

            final_message += '\n'
        
        #Another word sorter list, but this is for Coord_Word() subclass
        essential = WordSorter()
        filtered = self.__filter_stop_words(list([item for sub_list in sort_list for item in sub_list]))

        for i in filtered:
            essential.insert(i.word_to_coordword())
        
        essential_message = ""

        essential = [item for sub_list in essential.node_to_list() for item in sub_list]

        #get essential message 
        for i in essential:
            essential_message += i.get_word()
            essential_message += " "

        final_message += "*** Essential Message\n" + essential_message

        print(final_message)
        return final_message



    #Filter out the recognized stop words from mesage
    def __filter_stop_words(self, decoded_message):
        important = []

        if self.__stop_words == None:
            raise ValueError('Object stop word reference list not found use set_stop_words() method')
        #For each word in the decoded message, check if exist in stop word list
        for word in decoded_message:

            if word.get_word().lower() not in self.__stop_words:
                important.append(word)

        #Return list of important words only
        return important
    

    #Write a text file 
    def write_file(self, message):
        #Ensure that the text file is valid
        if self.__write_file == None or self.__write_file[-4:] != '.txt':
            raise ValueError('File is invalid or not set. Please set a proper .txt file using set_write_file()')

        if os.path.exists(os.path.split(self.__write_file)[0]):
            with open(self.__write_file, 'w') as f:
                f.write(message)
        else:
            directory = os.path.split(self.__write_file)[0]
            if directory != '':
                os.makedirs(directory)
            with open(self.__write_file, 'w') as f:
                f.write(message)
    

    #Request user morse message input from a file 
    def request_morse_from_file(self):
        #Checks the read path 
        readpath = ''
        while not os.path.isfile(readpath):
            readpath = input('\nPlease enter input file: ')

            #Try again if file path is non-existant
            if not os.path.isfile(readpath):
                print("Path does not exist")

        with open(current_dir + '\\' + readpath, 'r') as f:
            lines = f.read()
            self.set_morse_message(lines)

    
    #Request where to save content to file 
    def request_write_file(self):
        savepath = ''
        while savepath[-4:] != '.txt':
            savepath = input('Please enter output file: ')

            #If path does not end with a valid .txt extention
            try:
                self.set_write_file(savepath)
            except ValueError:
                print("Please enter a valid file extension .txt")


    #Default Morse does not have printing
    def __str__(self):
        return "Base Morse class has no printing, use MorseHorizontal() or MorseVertical()"


    #Set methods 
    #Set message to be decoded 
    def set_morse_message(self, morse_message):
        for letter in morse_message:
            #Check if txt file only contains allowed data '.'  ','  '-'  '\n'  and  'space'
            if letter not in self.__valid_morse:
                raise ValueError("Invalid Values in file. Please have a Text file with only '.' ',' '\\n' and ' ' ")
        
        self.__morse_message = morse_message


    #Edit stop words (custom list or using a file)
    def set_stop_words(self, stop_words_path):
        #Check if list or file path before setting stop words
        if isinstance(stop_words_path, list):
            self.__stop_words = list(map(lambda x: x.lower(), stop_words_path))

        elif not os.path.isfile(stop_words_path):
            raise FileNotFoundError("Please enter a valid path or input a custom python list")

        else:
            with open(current_dir+'\\'+ stop_words_path, 'r') as f:
                lines = f.read()
            self.__stop_words = lines.split('\n')    


    #Set a write file  
    def set_write_file(self, file_path):
        #If path does not end with a valid .txt extention
        if file_path[-4:] != '.txt':
            raise ValueError("Please enter a valid file extension .txt")

        else: 
            self.__write_file = file_path


    #Get methods for attribute retrieval
    def get_morse_message(self):
        return self.__morse_message

    def get_stop_words(self):
        return self.__stop_words

    def get_write_file(self):
        return self.__write_file
    
    def get_valid_morse(self):
        return self.__valid_morse

    #See translation sheet of Morse object
    def get_codes(self):
        return self.__codes
    
    
    
    #Change global morse values that are allowed (list of values)
    @classmethod
    def set_valid_morse(cls, morse_list):
        if isinstance(morse_list, list):
            cls.__valid_morse = morse_list
        else:
            raise TypeError("Please enter a list")


    #Static methods 
    #Meant for 2D list coordinates retrieval for each word
    @staticmethod
    def get_coordinates(item, decoded_message):
        source_list = [list(filter(None, i.split(' '))) for i in decoded_message.upper().split('\n')]
        coordinates = []

        #Retrieve row and column indexes of word
        for row, sub_list in enumerate(source_list):
            for column in range(len(sub_list)):
                if sub_list[column] == item.upper():
                    #Append coordinates
                    coordinates.append((row, column))

        #Returns list of coordinates of word in original message
        return coordinates

    #Get all unique values in decoded mesage 
    @staticmethod
    def get_unique(decoded_message):
        decoded_array = [list(filter(None, i.split(' '))) for i in decoded_message.split('\n')]
        unique = set([item.upper() for sub_list in decoded_array for item in sub_list])

        return unique


#Morse class that supports horizontal printing
class MorseHorizontal(Morse):

    #Convert Horizontal Morse to Vertical Morse class
    def hori_to_verti(self):
        return MorseVertical(self.get_stop_words(), self.letter_message, self.get_morse_message(), self.get_write_file())
            
    def __str__(self) :
        return self.encodeMorse()


#Morse class that supports vertical printing
class MorseVertical(Morse):
    def __str__(self):
        
        maxlen = 0
        letters = []
        #Split word from sentence
        for word in self.encodeMorse().split(): 
            
            #Split alphabets in each word
            for letter in word.split(','): 
                #Get max length/ longest alphabet
                if len(letter) > maxlen: 
                    maxlen = len(letter)
                letters.append(letter)
        
            for i in range(len(letters)):
                for n in range(maxlen - len(letters[i])):
                    letters[i] = " " + letters[i]
        
        final_line = ""

        for ix in range(maxlen): #How many words are there
            for w in letters:
                final_line += w[ix] 
            
            final_line += "\n"
        return final_line
    

    #Convert Vertical Morse to Horizontal Morse
    def verti_to_hori(self):
        return MorseHorizontal(self.get_stop_words() ,self.letter_message, self.get_morse_message(), self.get_write_file())
