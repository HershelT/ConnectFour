import os, sys
sys.path.insert(0, 'ImageReader')
from ImageReader import *
from loadscreen import *
from functions import *
LENGTHOFBOARD = 6
WIDTHOFBOARD = 7
#Using lambda to clear the screen 
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

#Creating the piece class
class Piece:
    def __init__(self, color):
        self.color = color
    def __str__(self):
        return self.color
    def __repr__(self):
        return self.color
#Creating the board class
class Board:
    def __init__(self):
        self.board = [[0 for i in range(WIDTHOFBOARD)] for j in range(LENGTHOFBOARD)]
    def placePiece(self, piece, BoardPieceColor, x):
        for i in range(0, len(self.board)):
            if isinstance(self.board[0][x], Piece):
                return False
            if isinstance(self.board[i][x], Piece) and i != 0:
                self.board[i-1][x] = piece
                addLinesToSreen(BoardPieceColor, BoardConnect, 6*(len(self.board) - (i-1)-1)+1, x*12 + 2, '\033[m', False)
                addLinesToSreen(BoardConnect, EmptyScreen, 5, 10, '\033[m', False)
                return True
            elif i == len(self.board)-1:
                self.board[i][x] = piece
                addLinesToSreen(BoardPieceColor, BoardConnect, 12*(len(self.board) - (i)-1)+1, x*12 + 2, '\033[m', False)
                addLinesToSreen(BoardConnect, EmptyScreen, 5, 10, '\033[m', False)
                return True
            addLinesToSreen(BoardPieceColor, BoardConnect, 6*(len(self.board) - (i)-1)+1, x*12 + 2, '\033[m', False)
            addLinesToSreen(BoardConnect, EmptyScreen, 5, 10, '\033[m', False)
            printScreen(EmptyScreen)
            time.sleep(0.1)
            addLinesToSreen(ERASEBLOCK, BoardConnect, 6*(len(self.board) - (i)-1)+1, x*12 + 2, '\033[m', False)
            addLinesToSreen(BoardConnect, EmptyScreen, 5, 10, '\033[m', False)
            printScreen(EmptyScreen)
            
            

    def placeWinPiece(self, piece, x, y):   
        addLinesToSreen(piece, BoardConnect, 6*(len(self.board) - (y)-1)+1, x*12 + 2, '\033[m', False)
    def checkWin(self, pieceColor):
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board[i])):
                if isinstance(self.board[i][j], Piece):
                    if self.checkWinPiece(i, j, pieceColor):
                        return True
        return False
    
    def blinkPieces(self, winPieceList, pieceColor):
        turns = 0
        if pieceColor == PIECERED:
            piece = WINPIECERED
        else:
            piece = WINPIECEYELLOW
        while turns < 11:
            if turns % 2 == 0:
                blinkingPiece = piece
            else:
                blinkingPiece = pieceColor
            for i in winPieceList[1]:
                self.placeWinPiece(blinkingPiece, i[1], i[0])
            addLinesToSreen(BoardConnect, EmptyScreen, 5, 10, '\033[m', False)
            printScreen(EmptyScreen)
            time.sleep(0.5)
            turns += 1
        return True
        
    def checkWinPiece(self, x, y, pieceColor):
        piece = self.board[x][y]
        verticals = self.checkWinVertical(y, piece)
        horizontals = self.checkWinHorizontal(x, y, piece)
        diagonals = self.checkWinDiagonal(x, y, piece)
        if verticals[0]:
            self.blinkPieces(verticals, pieceColor)
            return True
        if horizontals[0]:
            self.blinkPieces(horizontals, pieceColor)
            return True
        if diagonals[0]:
            self.blinkPieces(diagonals, pieceColor)
            return True
        return False
    def checkWinVertical(self, x, piece):
        count = 0
        positions = []
        for i in range(0, len(self.board)):
            if isinstance(self.board[i][x], Piece) and self.board[i][x].color == piece.color:
                count += 1
                positions.append((i, x))
                if count == 4:
                    return [True, positions]
            else:
                positions = []
                count = 0
        return [False]
    def checkWinHorizontal(self, x, y, piece):
        count = 0
        positions = []
        for j in range(0, len(self.board[y-1])):
            if isinstance(self.board[x][j], Piece) and self.board[x][j].color == piece.color:
                count += 1
                positions.append((x, j))
                if count == 4:
                    return [True, positions]
            else:
                positions = []
                count = 0
        return [False]
    def checkWinDiagonal(self, x, y, piece):
        for i in range(0, len(CHECKDIAGONALS)):
            count = 0
            positions = []
            for j in range(0, len(self.board)):
                if x+CHECKDIAGONALS[i][0]*j < 0 or x+CHECKDIAGONALS[i][0]*j >= len(self.board) or y+CHECKDIAGONALS[i][1]*j < 0 or y+CHECKDIAGONALS[i][1]*j >= len(self.board[0]):
                    break
                if isinstance(self.board[x+CHECKDIAGONALS[i][0]*j][y+CHECKDIAGONALS[i][1]*j], Piece) and self.board[x+CHECKDIAGONALS[i][0]*j][y+CHECKDIAGONALS[i][1]*j].color == piece.color:
                    count += 1
                    positions.append((x+CHECKDIAGONALS[i][0]*j, y+CHECKDIAGONALS[i][1]*j))
                    if count == 4:
                        return [True, positions]
                else:
                    positions = []
                    count = 0
        return [False]
    def __str__(self):
        result = ""
        for row in self.board:
            for col in row:
                if col == 0:
                    result += f"{black}|{reset}" + "0" + f"{black}|{reset}"
                else:
                    result += f"{black}|{reset}" + col.color + f"{black}|{reset}"
            result += "\n"
        result += f"{background_bright_blue}_____________________{reset}\n 0  1  2  3  4  5  6"
        return result
    def __repr__(self):
        return self.__str__()

#Function to move the piece to the board and check if the game is won
def MovePiece(col, type):
    if type[0] == "red":
        BoardPieceColor = PIECERED
        win = WINRED
        
    else:
        BoardPieceColor = PIECEYELLOW
        win = WINYELLOW
    if not b.placePiece(Piece(f'{type[1]} \033[0m'), BoardPieceColor ,col):
        return False
    elif b.checkWin(BoardPieceColor):
        clear()
        printScreen(EmptyScreen)
        print(reset)
        addLinesToSreen(win, EmptyScreen, len(EmptyScreen)-len(win), abs((int)(len(EmptyScreen[0])/2)-int((len(win[0])/2))), '\033[m', False)
        printScreen(EmptyScreen)
        print(f"{type[1]}{black}{type[0]} wins".capitalize(), end=reset)
        sys.exit()

#System for using arrow keys to drop pieces in the board in graphics
def selectingCol(piece):
    col = 3
    num = [0,0]
    currentCol = 12 * (col + 1)
    key_listener = MyKeyListener()
    listener = keyboard.Listener(
            on_press=key_listener.on_press,
            on_release=key_listener.on_release)
    listener.start()
    addLinesToSreen(piece, EmptyScreen, ROWOFDISPLAY, currentCol, '\033[m', False)
    printScreen(EmptyScreen)
    while not key_listener.is_enter_pressed() and not key_listener.is_down_arrow_pressed() and not key_listener.is_s_pressed():
        pressed = False
        if ((key_listener.is_left_arrow_pressed() or key_listener.is_a_pressed()) and col > 0): 
            num = [-12,-1]
            pressed = True
        elif ((key_listener.is_right_arrow_pressed() or key_listener.is_d_pressed()) and col < 6):  
            num = [12,1]
            pressed = True
        if pressed:
            addLinesToSreen(ERASEBLOCK, EmptyScreen, ROWOFDISPLAY, currentCol, '\033[m', False)
            currentCol += num[0]
            col += num[1]
            addLinesToSreen(piece, EmptyScreen, ROWOFDISPLAY, currentCol, '\033[m', False)
            key_listener.keys_pressed.discard(all); 
            printScreen(EmptyScreen)
            time.sleep(0.15)
        if key_listener.is_esc_pressed():
            print("You have exited the program")
            sys.exit()
        if key_listener.is_c_pressed():
            clear()
            printScreen(EmptyScreen)
    addLinesToSreen(convert_2d_array_to_empty_strings(PIECERED), EmptyScreen, ROWOFDISPLAY, currentCol, '\033[m', False)
    listener.stop()
    del listener
    return col    

 


#Creating Final variables for the display of the two pieces and how the 4 in a row gets checked
CHECKDIAGONALS = [(1, 1), (-1,1), (1, -1), (-1, -1)]
PIECEYELLOW    = AlternateConnectFourPieces.getPixelArray(0)
PIECERED       = AlternateConnectFourPieces.getPixelArray(1)
WINPIECERED    = AlternateConnectFourPieces.getPixelArray(2)
WINPIECEYELLOW = AlternateConnectFourPieces.getPixelArray(3)
ERASEBLOCK     = AlternateConnectFourPieces.getPixelArray(4)
WINRED = WinDisplay.getPixelArray(0)
WINYELLOW = WinDisplay.getPixelArray(1)

#Initializing the board graphics from the pixel art images
BoardConnect = AlternateConnectFourBoard.getPixelArray(0)
EmptyScreen  = AlternateConnectFourBoard.getPixelArray(1)
#Starting Screen and Pressed Start Screen
StartScreen  = AlternateConnectFourBoard.getPixelArray(2)
PressedStartScreen = AlternateConnectFourBoard.getPixelArray(3)
ROWOFDISPLAY = len(EmptyScreen)-len(PIECEYELLOW) -1

TextHighlight = '\033[48;5;32m'
# RegularColor =  '\033[48;5;12m'

#Initializing the board and pieces for behind the scenes game logic as well as the turn counter
turn = 0
b = Board()
p = Piece(f'{background_bright_red} \033[0m')

# Displaying the board

addLinesToSreen(BoardConnect, EmptyScreen, 5, 10, '\033[m', False)
addLinesToSreen(createArrayinArray("Selected Game Board (Press 'Tab'): \n  Original Board (Press 'Enter' to continue)"), StartScreen, 6, 8, TextHighlight+black, False)
clear()
# printScreen(EmptyScreen)
print(reset)

# Starting Game Loop to play the game
if __name__ == "__main__":
    printScreen(StartScreen)
    key_listener = MyKeyListener()
    listener = keyboard.Listener(
            on_press=key_listener.on_press,
            on_release=key_listener.on_release)
    listener.start()
    selection = 0
    while not key_listener.is_enter_pressed():
        if key_listener.is_esc_pressed():
            print("You have exited the program")
            time.sleep(0.5)
            sys.exit()
        if key_listener.is_c_pressed():
            clear()
            printScreen(StartScreen)
        if key_listener.is_tab_pressed() and selection % 2 == 0:
            BoardConnect = ConnectFourBoard.getPixelArray(0)
            EmptyScreen  = ConnectFourBoard.getPixelArray(1)
            PIECEYELLOW  = ConnectFourPieces.getPixelArray(0)
            PIECERED     = ConnectFourPieces.getPixelArray(1)
            WINPIECERED  = ConnectFourPieces.getPixelArray(2)
            WINPIECEYELLOW = ConnectFourPieces.getPixelArray(3)
            ERASEBLOCK     = ConnectFourPieces.getPixelArray(4)
            WINRED         = WinDisplay.getPixelArray(2)
            WINYELLOW      = WinDisplay.getPixelArray(3)
            StartScreen    = ConnectFourBoard.getPixelArray(2)
            PressedStartScreen = ConnectFourBoard.getPixelArray(3)
            addLinesToSreen(BoardConnect, EmptyScreen, 5, 10, '\033[m', False)
            TextHighlight = '\033[48;5;12m'
            addLinesToSreen(createArrayinArray("Selected Game Board (Press 'Tab' to change): \n  Modern Board (Press 'Enter' to continue)"), StartScreen, 6, 8, TextHighlight+black, False)
            # clear()
            printScreen(StartScreen)
            selection += 1
            time.sleep(0.2)
        elif key_listener.is_tab_pressed() and selection % 2 == 1:
            BoardConnect = AlternateConnectFourBoard.getPixelArray(0)
            EmptyScreen  = AlternateConnectFourBoard.getPixelArray(1)
            PIECEYELLOW  = AlternateConnectFourPieces.getPixelArray(0)
            PIECERED     = AlternateConnectFourPieces.getPixelArray(1)
            WINPIECERED  = AlternateConnectFourPieces.getPixelArray(2)
            WINPIECEYELLOW = AlternateConnectFourPieces.getPixelArray(3)
            ERASEBLOCK     = AlternateConnectFourPieces.getPixelArray(4)
            WINRED         = WinDisplay.getPixelArray(0)
            WINYELLOW      = WinDisplay.getPixelArray(1)
            StartScreen    = AlternateConnectFourBoard.getPixelArray(2)
            PressedStartScreen = AlternateConnectFourBoard.getPixelArray(3)
            addLinesToSreen(BoardConnect, EmptyScreen, 5, 10, '\033[m', False)
            TextHighlight = '\033[48;5;32m'
            addLinesToSreen(createArrayinArray("Selected Game Board (Press 'Tab' to change): \n  Original Board (Press 'Enter' to continue)"), StartScreen, 6, 8, TextHighlight+black, False)
            # clear()
            printScreen(StartScreen)
            selection += 1
            time.sleep(0.2)
            # addLinesToSreen(BoardConnect, EmptyScreen, 5, 10, '\033[m', False)

            

    
    # waitForInput('')
    printScreen(PressedStartScreen)
    sleepTime = 0.1
    loadGame = "Loading Game: \n"
    loadBar = ""
    for i in range(1,40):
        if key_listener.is_esc_pressed():
            print("You have exited the program")
            time.sleep(0.5)
            sys.exit()
        if key_listener.is_s_pressed():
            break
        addLinesToSreen(loadGame, PressedStartScreen, 7, 36, TextHighlight+yellow)
        addLinesToSreen(createEmptyString(loadBar), PressedStartScreen, 4, 25, TextHighlight+yellow)
        if i == 10: loadGame =  "Preping Assets:";sleepTime=0.2
        elif i == 20: loadGame = "Prepping Graphics:"; sleepTime=0.1
        addLinesToSreen(loadBar, PressedStartScreen, 4, 26, TextHighlight+red)
        loadBar +=  "#"
        printScreen(PressedStartScreen)
        time.sleep(sleepTime)
    listener.stop()
    del listener
    time.sleep(0.8)
    clear()
    printScreen(EmptyScreen)
    while True:
        if turn % 2 == 0:
            pieceColor = ["red", background_bright_red, PIECERED]
        else:
            pieceColor = ["yellow", background_yellow, PIECEYELLOW]
        # clear()
        printScreen(EmptyScreen)
        # printScreen(BoardConnect)
        colForPiece = selectingCol(pieceColor[2])
        if  MovePiece(colForPiece, pieceColor) == False:
            # turn -= 1
            continue
        turn += 1




    
