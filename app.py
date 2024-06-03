####################################################################
# ST1507 DSAA: MorseCode Message Analyzer (Morse Class)            #
#------------------------------------------------------------------#
#                                                                  #
# - Name: Aw Shao Yang                                             #
# - Class: DAAA/FT/2B/03                                           #
# - Admission Number: p2012126                                     #
####################################################################


from MorseTool import MorseHorizontal
from MorseTool import MorseVertical

#General Input function for user input 1 to 4
def get_input():
    choice = 0
    choices = [1,2,3,4]
    print("""\n\nPlease select your choice ('1','2','3','4'):
    1. Change Printing Mode
    2. Convert Morse Code To Text
    3. Analyze Morse Code Message
    4. Exit """)

    #Only possible choices are 1 to 4, else ask agian
    while choice not in choices:
        try: 
            choice = int(input("Enter choice: "))
        except ValueError:
            print("Please enter a number 1 to 4")
    return choice



def start():
    choice = 0

    #application creates the MorseHorizontal Object
    morse_obj = MorseHorizontal('../stop-words.txt')
    printing_mode = 'horizontal'
    while choice != 4:
        print("\n**********************************************************\n* ST1507 DSAA: MorseCode Message Analyzer                *\n*--------------------------------------------------------*\n*                                                        *\n*   - Done by: Aw Shao Yang (2012126)                    *\n*   - Class: DAAA/2B/03                                  *\n**********************************************************")
        choice = get_input()

        #Converting from h to v or v to h
        if choice == 1:
            printables = ['h','v']
            print_state = ''
            print(f"Current print mode is {printing_mode}")

            #Ensure proper input
            while print_state not in printables:
                print_state = input('Enter h for horizontal, Enter v for vertical then press enter: ').lower()
            
            #If requesting for convert to horizontal
            if print_state == 'h':
                
                #Check current object type
                if isinstance(morse_obj, MorseHorizontal):
                    print('Printing is already horizontal')
                else:

                    #Use convert MorseVertical to MorseHorizontal 
                    morse_obj = morse_obj.verti_to_hori()
                    print('The print mode has been changed to horizontal')
                    printing_mode = 'horizontal'

            #If requestion for convert to vertical
            if print_state == 'v':
                #Check current object type
                if isinstance(morse_obj, MorseVertical):
                    print('Printing is already vertical')
                else:

                    #Use convert MorseHorizontal to MorseVertical 
                    morse_obj = morse_obj.hori_to_verti()
                    print('The print mode has been changed to vertical')
                    printing_mode = 'vertical'
            input('\nPress Enter, to continue....')
                    
        #Output message 
        elif choice == 2:

            #Use object morse encoder method
            message = str(input("Please type text you want to convert to morse code:\n"))
            morse_obj.letter_message = message

            #Print output is different for Vert and Horizontal Morse
            print(morse_obj)
            input('\nPress Enter, to continue....')
        
        elif choice == 3:
            #Request files, analyze and then write to file
            try:
                morse_obj.request_morse_from_file()
                morse_obj.request_write_file()
                analyzed_content = morse_obj.analyze()
                morse_obj.write_file(analyzed_content)
            except ValueError:
                print("Invalid Values in file. Please have a Text file with only '.' ',' '\\n' and ' '")
            
        else:
            continue

    print('Bye thanks for using ST1507 DSAA: MorseCode Message Analyzer')

#Testing Ground
if __name__ == "__main__":
    start()