import time
import os, sys
import io
# from AsciiAnimations import *
from keyboardListener import *
from functions import *
#import image processor
sys.path.insert(0, 'ImageReader')
from ImageReader import *

clear_command = 'cls' if os.name == 'nt' else 'clear'
os.system(clear_command)

def waitForInput(char):
    user_input = None
    while (user_input != char):
        user_input = input()
# 
# 
# 
# 

def printScreen(screen, clear = True):
    # Create an off-screen buffer
    buffer = io.StringIO()

    for row in screen:
        # Write to the buffer instead of directly to the screen
        buffer.write(''.join(row) + '\033[0m\n')

    if clear:
        sys.stdout.write('\033[?25l')
        # Move the cursor to the top of the terminal
        sys.stdout.write('\033[H\033[?25l')

    # Swap the buffer with the screen
    sys.stdout.write(buffer.getvalue()+reset)
    sys.stdout.flush()

    # Clear the buffer for the next frame
    buffer.close()

#Adds text to overwrite over main screen with a specific row from most bottom of text being rowIndex from bottom of screen and column from left
def addLinesToSreen(lines, screen, rowIndex=0, colIndex=0, color='\033[m', createArray = True):
    if createArray: newLines = createArrayinArray(lines)
    else: newLines= lines
    for i, row in enumerate(newLines):
        for j, char in enumerate(row):
            screen[len(screen) - (len(newLines)+rowIndex)+i][colIndex+j] = color + char.replace('\033[0m', '') + '\033[0m'
#Use this after addlinestotext to erase a line written on previously
def convert_2d_array_to_empty_strings(array_2d):
    return [[' ' for _ in sublist] for sublist in array_2d]
#Creates a string of spaces and new lines from a list of strings
def createEmptyString(screenList : str):
    emptyString = ''.join(' ' if char != '\n' else '\n' for char in screenList)
    return emptyString

#Moves a character left or right (entity, screen it should be on,row want to be on, column want to be on, how much to move by, color if want)
def check_keys():
    key_listener = MyKeyListener()
    while (not key_listener.is_enter_pressed()):
        key_listener.check_keys()
        time.sleep(0.1)
    keyboard.Controller().release(keyboard.Key.enter)
    del key_listener