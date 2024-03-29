import os, sys
sys.path.insert(0, 'ImageReader')
from ImageReader import *
from loadscreen import *
from functions import *
LENGTHOFBOARD = 8
WIDTHOFBOARD = 8
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
                addLinesToSreen(BoardConnect, EmptyScreen, 0, 16, '\033[m', False)
                return True
            elif i == len(self.board)-1:
                self.board[i][x] = piece
                addLinesToSreen(BoardPieceColor, BoardConnect, 12*(len(self.board) - (i)-1)+1, x*12 + 2, '\033[m', False)
                addLinesToSreen(BoardConnect, EmptyScreen, 0, 16, '\033[m', False)
                return True
            addLinesToSreen(BoardPieceColor, BoardConnect, 6*(len(self.board) - (i)-1)+1, x*12 + 2, '\033[m', False)
            addLinesToSreen(BoardConnect, EmptyScreen, 0, 16, '\033[m', False)
            printScreen(EmptyScreen)
            time.sleep(0.1)
            addLinesToSreen(EMPTYGREEN, BoardConnect, 6*(len(self.board) - (i)-1)+1, x*12 + 2, '\033[m', False)
            addLinesToSreen(BoardConnect, EmptyScreen, 0, 16, '\033[m', False)
            printScreen(EmptyScreen)
        # return True
            
            

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
        if pieceColor == PIECEWHITE:
            piece = WINPIECEGOLD
        else:
            piece = WINPIECEBLACKGOLD
        while turns < 10:
            if turns % 2 == 0:
                blinkingPiece = piece
            else:
                blinkingPiece = pieceColor
            for i in winPieceList[1]:
                self.placeWinPiece(blinkingPiece, i[1], i[0])
            addLinesToSreen(BoardConnect, EmptyScreen, 0, 16, '\033[m', False)
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
                # print(count)
                # time.sleep(0.5)
                positions.append((i, x))
                if count == 4:
                    return [True, positions]
            else:
                positions = []
                count = 0
        return [False, positions]
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
        return [False, positions]
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
        return [False, positions]
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
    if type[0] == "white":
        BoardPieceColor = PIECEWHITE
    else:
        BoardPieceColor = PIECEBLACK
    if not b.placePiece(Piece(f'{type[1]} \033[0m'), BoardPieceColor ,col):
        return False
    if MovePiece.white + 4 >= len(EmptyScreen) or MovePiece.black + 4 >= len(EmptyScreen):
        MovePiece.white = -1
        MovePiece.black = -1
    if type[0] == "white":
        addLinesToSreen(ERASEBLOCK, EmptyScreen, MovePiece.white+4, len(EmptyScreen[0])-14, '\033[m', False)
        MovePiece.white += 2
    else:
        addLinesToSreen(ERASEBLOCK, EmptyScreen, MovePiece.black+4, 2, '\033[m', False)
        MovePiece.black += 2
    if b.checkWin(BoardPieceColor):
        clear()
        printScreen(EmptyScreen)
        print(reset)
        print(f"{type[0]} wins")
        sys.exit()

#System for using arrow keys to drop pieces in the board in graphics
def selectingCol(piece):
    col = 3
    currentCol = 12 * (col + 1) + 6
    key_listener = MyKeyListener()
    listener = keyboard.Listener(
            on_press=key_listener.on_press,
            on_release=key_listener.on_release)
    listener.start()
    addLinesToSreen(piece, EmptyScreen, ROWOFDISPLAY-1, currentCol, '\033[m', False)
    printScreen(EmptyScreen)
    while not key_listener.is_enter_pressed() and not key_listener.is_down_arrow_pressed() and not key_listener.is_s_pressed():
        if ((key_listener.is_left_arrow_pressed() or key_listener.is_a_pressed()) and col > 0) or ((key_listener.is_right_arrow_pressed() or key_listener.is_d_pressed()) and col < WIDTHOFBOARD-1):
            if key_listener.is_right_arrow_pressed() or key_listener.is_d_pressed():
                num = [12,1]
            else:
                num = [-12,-1]
            addLinesToSreen(EMPTYGREEN, EmptyScreen, ROWOFDISPLAY-1, currentCol, '\033[m', False)
            currentCol += num[0]
            col += num[1]
            addLinesToSreen(piece, EmptyScreen, ROWOFDISPLAY-1, currentCol, '\033[m', False)
            key_listener.keys_pressed.discard(all); 
            printScreen(EmptyScreen)
            time.sleep(0.15)
        if key_listener.is_esc_pressed():
            print("You have exited the program")
            sys.exit()
        if key_listener.is_c_pressed():
            clear()
            printScreen(EmptyScreen)
    addLinesToSreen(EMPTYGREEN, EmptyScreen, ROWOFDISPLAY-1, currentCol, '\033[m', False)
    listener.stop()
    del listener
    return col   
 
#Creating Final variables for the display of the two pieces and how the 4 in a row gets checked
CHECKDIAGONALS = [(1, 1), (-1,1), (1, -1), (-1, -1)]
PIECEBLACK = OthelloPieces.getPixelArray(0)
PIECEWHITE = OthelloPieces.getPixelArray(1)
WINPIECEGOLD = OthelloPieces.getPixelArray(3)
WINPIECEBLACKGOLD = OthelloPieces.getPixelArray(3)
EMPTYGREEN = OthelloPieces.getPixelArray(2)
ERASEBLOCK = OthelloPieces.getPixelArray(4)

#Initializing the board graphics from the pixel art images
BoardConnect = OthelloBoard.getPixelArray(0)
EmptyScreen = OthelloBoard.getPixelArray(1)
ROWOFDISPLAY = len(EmptyScreen)-len(PIECEBLACK)

#Making pieces disapear


#Initializing the board and pieces for behind the scenes game logic as well as the turn counter
turn = 0
b = Board()
p = Piece(f'{background_bright_red} \033[0m')

# Displaying the board
addLinesToSreen(BoardConnect, EmptyScreen, 0, 16, '\033[m', False)
clear()
# printScreen(EmptyScreen)
print(reset)
MovePiece.white = -1
MovePiece.black = -1
# Starting Game Loop to play the game
if __name__ == "__main__":
    
    # printScreen(OthelloBoard.getPixelArray(2))
    # waitForInput('')
    # printScreen(OthelloBoard.getPixelArray(3))
    # sleepTime = 0.1
    # loadGame = "Loading Game: \n"
    # loadBar = ""
    # for i in range(1,40):
    #     addLinesToSreen(loadGame, OthelloBoard.getPixelArray(3), 7, 36, '\033[48;5;12m'+yellow)
    #     addLinesToSreen(createEmptyString(loadBar), OthelloBoard.getPixelArray(3), 4, 25, '\033[48;5;12m'+yellow)
    #     if i == 10: loadGame =  "Preping Assets:";sleepTime=0.2
    #     elif i == 20: loadGame = "Prepping Graphics:"; sleepTime=0.1
    #     addLinesToSreen(loadBar, OthelloBoard.getPixelArray(3), 4, 26, '\033[48;5;12m'+red)
    #     loadBar +=  "#"
    #     printScreen(OthelloBoard.getPixelArray(3))
    #     time.sleep(sleepTime)
    # time.sleep(0.8)
    clear()
    printScreen(EmptyScreen)
    while True:
        if turn % 2 == 0:
            pieceColor = ["white", background_bright_red, PIECEWHITE]
        else:
            pieceColor = ["black", background_yellow, PIECEBLACK]
        # clear()
        printScreen(EmptyScreen)
        # print(b)
        # printScreen(BoardConnect)
        colForPiece = selectingCol(pieceColor[2])
        if  MovePiece(colForPiece, pieceColor) == False:
            # turn -= 1
            continue
        turn += 1