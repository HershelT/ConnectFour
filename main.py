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
            elif isinstance(self.board[i][x], Piece) and i != 0:
                self.board[i-1][x] = piece
                addLinesToSreen(BoardPieceColor, BoardConnect, 6*(len(self.board) - (i-1)-1)+1, x*12 + 2, '\033[m', False)
                addLinesToSreen(BoardConnect, EmptyScreen, 6, 10, '\033[m', False)
                return True
            elif i == len(self.board)-1:
                self.board[i][x] = piece
                addLinesToSreen(BoardPieceColor, BoardConnect, 12*(len(self.board) - (i)-1)+1, x*12 + 2, '\033[m', False)
                addLinesToSreen(BoardConnect, EmptyScreen, 6, 10, '\033[m', False)
                return True
    def checkWin(self):
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board[i])):
                if isinstance(self.board[i][j], Piece):
                    if self.checkWinPiece(i, j):
                        return True
        return False
    def checkWinPiece(self, x, y):
        piece = self.board[x][y]
        if self.checkWinVertical(x, piece):
            return True
        if self.checkWinHorizontal(x, y, piece):
            return True
        if self.checkWinDiagonal(x, y, piece):
            return True
        return False
    def checkWinVertical(self, x, piece):
        count = 0
        for i in range(0, len(self.board)):
            if isinstance(self.board[i][x], Piece) and self.board[i][x].color == piece.color:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
        return False
    def checkWinHorizontal(self, x, y, piece):
        count = 0
        for j in range(0, len(self.board[y-1])):
            if isinstance(self.board[x][j], Piece) and self.board[x][j].color == piece.color:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
        return False
    def checkWinDiagonal(self, x, y, piece):
        for i in range(0, len(CHECKDIAGONALS)):
            count = 0
            for j in range(0, len(self.board)):
                if x+CHECKDIAGONALS[i][0]*j < 0 or x+CHECKDIAGONALS[i][0]*j >= len(self.board) or y+CHECKDIAGONALS[i][1]*j < 0 or y+CHECKDIAGONALS[i][1]*j >= len(self.board[0]):
                    break
                if isinstance(self.board[x+CHECKDIAGONALS[i][0]*j][y+CHECKDIAGONALS[i][1]*j], Piece) and self.board[x+CHECKDIAGONALS[i][0]*j][y+CHECKDIAGONALS[i][1]*j].color == piece.color:
                    count += 1
                    if count == 4:
                        return True
                else:
                    count = 0
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
    else:
        BoardPieceColor = PIECEYELLOW
    if not b.placePiece(Piece(f'{type[1]} \033[0m'), BoardPieceColor ,col):
        return False
    elif b.checkWin():
        clear()
        printScreen(EmptyScreen)
        print(reset)
        print(f"{type[0]} wins")
        sys.exit()

#System for using arrow keys to drop pieces in the board in graphics
def selectingCol(piece):
    col = 3
    currentCol = 12 * (col + 1)
    key_listener = MyKeyListener()
    listener = keyboard.Listener(
            on_press=key_listener.on_press,
            on_release=key_listener.on_release)
    listener.start()
    emptyString = convert_2d_array_to_empty_strings(piece)
    addLinesToSreen(piece, EmptyScreen, ROWOFDISPLAY, currentCol, '\033[m', False)
    printScreen(EmptyScreen)
    while not key_listener.is_enter_pressed() and not key_listener.is_down_arrow_pressed():
        if (key_listener.is_left_arrow_pressed() and col > 0) or (key_listener.is_right_arrow_pressed() and col < 6):
            if key_listener.is_right_arrow_pressed():
                num = [12,1]
            else:
                num = [-12,-1]
            addLinesToSreen(emptyString, EmptyScreen, ROWOFDISPLAY, currentCol, '\033[m', False)
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
PIECEYELLOW = ConnectFourPieces.getPixelArray(0)
PIECERED = ConnectFourPieces.getPixelArray(1)

#Initializing the board graphics from the pixel art images
BoardConnect = ConnectFourBoard.getPixelArray(0)
EmptyScreen = ConnectFourBoard.getPixelArray(1)
ROWOFDISPLAY = len(EmptyScreen)-len(PIECEYELLOW)


#Initializing the board and pieces for behind the scenes game logic as well as the turn counter
turn = 0
b = Board()
p = Piece(f'{background_bright_red} \033[0m')

# Displaying the board
addLinesToSreen(BoardConnect, EmptyScreen, 6, 10, '\033[m', False)
clear()
printScreen(EmptyScreen)
print(reset)

# Starting Game Loop to play the game
if __name__ == "__main__":
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




    
