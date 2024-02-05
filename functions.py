#Creating pixel creater

from keyboardListener import *
import re
sys.path.insert(0, 'ImageReader')
from ImageReader import *

def createArrayinArray(text: str):
    rows = text.splitlines()
    # If the first line is empty, skip it
    if rows and not rows[0]:
        rows = rows[1:]
    # If the last line is empty, skip it
    if rows and not rows[-1]:
        rows = rows[:-1]
    # newText = [list(row) for row in rows]
    # return newText
    newText = []
    current_color = ''
    for line in rows:
        row = []
        segments = re.split(r'(\{.*?\})', line)
        for segment in segments:
            if segment.startswith('{') and segment.endswith('}') and segment[1:-1] in colors:
                current_color = colors[segment[1:-1]]
            else:
                row.extend([current_color + char for char in segment])
        newText.append(row)
    return newText
class PixelDesigner:
    def __init__(self, entity : str) -> None:
        self.entity = entity
        rows = entity.splitlines()
        # If the first line is empty, skip it
        if rows and not rows[0]:
            rows = rows[1:]
        # If the last line is empty, skip it
        if rows and not rows[-1]:
            rows = rows[:-1]
        self.pixelEntity = [list(row) for row in rows]
    def ChangeRow(self, row, rowText, color= "\033[0m"):
        for i in range(0, len(rowText)):
            self.pixelEntity[row][i] = color + rowText[i]
    def setPixelRowCol(self, row, col, pixel):
        self.pixelEntity[row,col] = pixel
    def getEntity(self):
        return self.entity
    def replaceChar(self, char, newChar, color= "\033[0m"):
        for row in range(0, len(self.pixelEntity)):
            for col in range(0, len(self.pixelEntity[row])):
                if self.pixelEntity[row][col] == char:
                    self.pixelEntity[row][col] = color + newChar
    def replaceString(self, string, newString, color= "\033[0m"):
        for i, row in enumerate(self.pixelEntity):
            for j, col in enumerate(row):
                if j+len(string) > len(row): 
                    continue
                result = ""
                for c in range(0, len(string)):
                    result += self.pixelEntity[i][j+c]
                if ansi_escape.sub('', result) == string:
                    for c in range(0, len(string)):
                        self.pixelEntity[i][j+c] = color + newString[c]
                    return True
        else:
            return False                       
    def replaceMultiLineString(self, strings, newStrings, color="\033[0m"):
        if not isinstance(strings, list):
            strings = createArrayinArray(strings)
        if not isinstance(newStrings, list):
            newStrings = createArrayinArray(newStrings)
        
        if len(strings) != len(newStrings):
            return False
        rowsToReplace = []
        count = 0
        for l in range(0, len(strings)):
            for i, row in enumerate(strings):
                for j, col in enumerate(strings[i]):
                    result = []
                    for c in range(0, len(strings[i])):
                        result.append(self.pixelEntity[i][j+c])
                    if result == strings[i]:
                        count+=1
                        rowsToReplace.append(i)
                        continue
                
                if count == len(strings):
                    for n in range(0, len(rowsToReplace)):
                        self.pixelEntity[rowsToReplace[n]] = newStrings[n]
                    return True                    

    def getPixelizedEntity(self):
        return self.pixelEntity