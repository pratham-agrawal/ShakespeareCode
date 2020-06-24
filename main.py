import logging
logging.basicConfig(filename='debug.txt', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
from random import *
punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
file = open('RANDOMLINES.txt', 'w')
file.write("RANDOM LINES:" + '\n')
file.close()

def openFile(fileName):
  '''
  Opensfiles
  
  Takes in file name, returns a list that doesn't have any newlines 

  Parameters
  ----------
  filename : string
    The name of the file
  
  Returns
  -------
  list
    File without newlines
  None
    If error occurs
  '''
  logging.debug('Starting with openfile name of ' + str(fileName))
  try:
    file = open(fileName, 'r')
    fileContents = file.readlines()
    file.close()
    text = []
    for i in fileContents:
      newLine = i.strip("\n")
      text.append(newLine)  
    logging.debug('File written')
    return text
  except FileNotFoundError:
    print("The text does not exist")
    logging.debug('Exception called')
    return None
    
def characterListAndLines(text):
  '''
  Sorts all characters and lines
  
  Adds each characters quote into a list in a dictionary 

  Parameters
  ----------
  text : list
    The entire play
  
  Returns
  -------
  Dict
    Dictionary containg all characters lines

  Raises
  ------
  TypeError
    If text is not a list
  '''
  logging.debug('Starting to write dictionary of character lines')
  if not isinstance(text, list):  
    raise TypeError('Expecting a list')
  else:
    charDictionary = {}
    for i in text:
      if i.isupper() and i not in charDictionary.keys() and i.startswith("ACT") != True:
        charDictionary.update( {i: []} )
    for lineCount in range(0, len(text) - 1, 1):
      if text[lineCount] in charDictionary.keys():
        charName = text[lineCount]
        lineCount += 1
        quote = ""
        while text[lineCount] not in charDictionary.keys() and lineCount < len(text) -1 and text[lineCount] != '' and text[lineCount + 1] != '':
          quote += str(text[lineCount]) + "\n"
          lineCount += 1
        charDictionary[charName].append(quote)
    logging.debug('Finished writing dictionary')
    return charDictionary

def userInput(choice):
  '''
  Formats users choice
  
  Splits input and formats the first part so that it matches text files and splits scond part so it matches characters

  Parameters
  ----------
  choice : string
    User's input
  
  Returns
  -------
  list
    Formatted input
  none
    If error occurs'''
  logging.debug('Starting with choice name of ' + str(choice))
  try:
    splitChoice = choice.split(', ')
    splitChoice[0] = splitChoice[0].replace(" ", "")
    splitChoice[0] = str(splitChoice[0]).upper() + '.txt'
    splitChoice[1] = str(splitChoice[1]).upper()
    logging.debug('Finsihed formatting string')
    return splitChoice
  except:
    print("The text and word should be seperated by a ', '")
    logging.debug('Exception thrown')
    return None

logging.debug('Start of program')

run = True
while run == True:
  menu = input('''
  ------------------------------------------

  What do you want to do?
  1. Randomly generate a quote
  2. Guess how many times a character speaks
  3. Find the number of word occurrences
  4. Exit 
  
  ------------------------------------------
  ''')

  if menu == '1':
    logging.debug('Starting of menu 1')
    choice = input("Enter the text and the character name separated by ', '" + '\n')
    splitChoice = userInput(choice)
    if splitChoice != None:
      text = (openFile(splitChoice[0]))
      if text != None:
        charDictionary = characterListAndLines(text)
        if splitChoice[1] in charDictionary:
          random = randint(1, len(charDictionary[splitChoice[1].upper()]))
          print(charDictionary[splitChoice[1].upper()][random])
          file = open('RANDOMLINES.txt', 'a')
          file.write(str(splitChoice[0]) + ', ' + str(splitChoice[1]) + ':' +'\n' + charDictionary[splitChoice[1].upper()][random] + '\n')
          file.close()
        else:
          print("Character doesn't exist")

  elif menu == '2':
    logging.debug('Starting of menu 2')
    choice = input("Enter the text and the character name separated by ', '" + '\n')
    splitChoice = userInput(choice)
    if splitChoice != None:
      text = (openFile(splitChoice[0]))
      if text != None:
        charDictionary = characterListAndLines(text)
        if splitChoice[1] in charDictionary:
          guessCounter = 0
          while True:
            guessCounter += 1
            guess = input("Enter your guess" + '\n')
            try:
              intGuess = int(guess)
              if intGuess == len(charDictionary[splitChoice[1].upper()]):
                print("You are correct, it took you " + str(guessCounter) + " attempt(s) to guess the right answer")
                break
              elif int(guess) > len(charDictionary[splitChoice[1].upper()]):
                print("Wrong answer, the real answer is lower")
              elif int(guess) < len(charDictionary[splitChoice[1].upper()]):
                print("Wrong answer, the real answer is higher")
              contin = input("Would you like to continue guessing? 'Yes' or 'No'" + '\n')
              if contin.lower() == 'yes':
                pass
              if contin.lower() == 'no':
                print("The real answer was " + str(len(charDictionary[splitChoice[1].upper()])))
                break
              if contin.lower() != 'yes' and contin.lower() != 'no':
                print("Invalid input")
                break
            except Exception as e:
              print("Must be an int")
        else:
          print("Character doesn't exist")
      
  elif menu =='3':
    logging.debug('Starting of menu 3')
    counter = 0
    choice = input("Enter the text and the word separated by ', '" + '\n')
    splitChoice = userInput(choice)
    if splitChoice != None:
      text = openFile(splitChoice[0]) 
      if text != None:
        for line in text:
          splitLine = line.split()
          for word in splitLine:
            newWord = []
            for char in word:
              if char not in punctuations:
                newWord += char
              elif len(newWord) > 0:
                break
            newWord = ''.join(newWord)
            if newWord.upper() != newWord:
              if newWord.upper() == splitChoice[1]:
                counter += 1
        print(counter)
    
  elif menu == '4':
    logging.debug('Program is ended')
    run = False

  else:
    logging.debug('Invalid input from user ' + str(menu))
    print("Invalid input")
