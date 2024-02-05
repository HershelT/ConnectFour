import re
reset = "\033[0m"
black = "\033[30m"
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
magenta = "\033[35m"
cyan = "\033[36m"
white = "\033[37m"
bright_black = "\033[90m"
bright_red = "\033[91m"
bright_green = "\033[92m"
bright_yellow = "\033[93m"
bright_blue = "\033[94m"
bright_magenta = "\033[95m"
bright_cyan = "\033[96m"
bright_white = "\033[97m"
background_red = "\033[41m"
background_green = "\033[42m"
background_yellow = "\033[43m"
background_blue = "\033[44m"
background_magenta = "\033[45m"
background_cyan = "\033[46m"
background_white = "\033[47m"
background_bright_black = "\033[100m"
background_bright_red = "\033[101m"
background_bright_green = "\033[102m"
background_bright_yellow = "\033[103m"
background_bright_blue = "\033[104m"
background_bright_magenta = "\033[105m"
background_bright_cyan = "\033[106m"
background_bright_white = "\033[107m"
background_black = "\033[40m"
background_purple = "\033[48;5;54m"
background_light_blue = "\033[48;5;39m"
ansi_escape = re.compile(r'\033\[\d+m')
colors = {
    #colors
    'w': white, 'r': red, 'g': green, 'b': blue, 
    'y': yellow, 'm': magenta, 'c': cyan, 
    #bright colors
    'W': bright_white, 'R': bright_red, 'G': bright_green, 'B': bright_blue,
    'Y': bright_yellow, 'M': bright_magenta, 'C': bright_cyan, 
    #background colors
    'Wb': background_bright_white, 'Rb': background_bright_red, 'Gb': background_bright_green, 
    'Bb': background_bright_blue, 'Yb': background_bright_yellow, 'Mb': background_bright_magenta,
    'Cb': background_bright_cyan, 'Lb' : background_light_blue,
    
    #reset
    '0' : reset,
              }