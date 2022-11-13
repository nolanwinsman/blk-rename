import os # used to loop through folder and rename files
import sys # used for arguments
import shlex # used to get arguments from input()
import os # used to clear the screen
import re # regex
import readline # including this package allows y

# NOTE
# in .bashrc add
# alias bulk_renamer='sudo python3 <path to .py script> "$PWD"'

# TODO
# comments
# README.md new utilities
# append function
# insert function

# the directory this script is working on
DIR = ""

# extensions of files we want to rename
# changes this or use the arguments to use different file extensions
EXTENSIONS = ['.mp4', '.mkv', '.mov', '.avi']
ALL_FILES = False # boolean for if every file in DIR should be added to dictionary files
files = {}


HIDE = False


class file_struct():
    """Struct to organize the files the script will rename
    """
    def __init__(self, original, path, ext):
        self.original = original
        self.path = path
        self.new = [original]
        self.ext = ext
        self.display = [True]

def replace_str(old, new):
    """ Replaces the old string with the new string

    Parameters :
    old -- string to be replaced
    new -- string that replaces old
    """
    for key, elem in files.items():
        temp = elem.new[-1]
        temp = temp.replace(elem.ext, "") # removes the extension so that the replace will not affect it
        temp = temp.replace(old, new) # replaces old string with new string
        temp = f"{temp}{elem.ext}" # adds back the extension
        add_new(key, temp)

def range_replace(min_r, max_r, old, new):
    print("made it to func")
    min_r, max_r = int(min_r), int(max_r)

    # if the min value is greater than the max value, swaps the values
    if min_r > max_r:
        min_r, max_r = max_r, min_r

    if min_r < 0 or max_r < 0:
        print("Invalid arguments")
        return

    for key, elem in files.items():
        temp = elem.new[-1]
        try:
            num = int(re.search(r'\d+', temp).group()) # attempts to find a number
        except Exception as e:
            print(f"Exception {e} occured")
            continue

        if num >= min_r and num <= max_r:
            temp = temp.replace(elem.ext, "") # removes the extension so that the replace will not affect it
            temp = temp.replace(old, new) # replaces old string with new string
            print(f"if statement temp: \n{temp}\nNEW: {new}")
            temp = f"{temp}{elem.ext}" # adds back the extension
            add_new(key, temp)
        else:
            add_new(key, elem.new[-1])

def remove_from_end(n):
    """Removes the last n chars (excluding the extension) from the files in files{}
    """
    for key, elem in files.items():
        temp = elem.new[-1]
        print(f"EXT\t{elem.ext}")
        # removes last n characters from string except for the extension
        temp = temp.replace(elem.ext, "")
        length = len(temp) - n
        add_new(key, f"{temp[:length]}{elem.ext}")

def remove_from_middle(left, right):
    for key, elem in files.items():
        temp = elem.new[-1]
        temp = temp.replace(elem.ext, "") # removes the extension so that the replace will not affect it
        add_new(key, f"{temp[:left]}{temp[right:]}{elem.ext}")

def remove_from_front(n):
    """ Removes the first n chars from the files in files{}
    """
    for key, elem in files.items():
        temp = elem.new[-1]
        temp = temp.replace(elem.ext, "")
        # removes first n characters from string
        add_new(key, f"{temp[n:]}{elem.ext}")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_current():
    """Prints what the files will be renamed to if rename_files() is called
    """
    # clear_screen()
    print("-----Current Iteration of Changes-----")
    for elem in files.values():
        if elem.display[-1]:
            print(elem.new[-1])

def insert_text(position, text):
    for key, elem in files.items():
        temp = elem.new[-1]
        temp = temp.replace(elem.ext, "") # removes the extension so that the insert will not affect it
        # edge case to add text to the end
        if position <= -1:
            add_new(key, f"{temp}{text}{elem.ext}")
        else:
            add_new(key, f"{temp[:position]}{text}{temp[position:]}{elem.ext}")

def undo():
    """ Redacts the last change the user input in loop()
    """
    for elem in files.values():
        assert len(elem.new) == len(elem.display)
        if len(elem.new) > 1:
            elem.new.pop()
            elem.display.pop()

def add_new(key, new_text):
    length = len(files[key].display)
    print(f"The new text: {new_text}")
    if length > 1:
        prev = files[key].display[length - 1]
    else:
        prev = True
    files[key].display.append(prev)
    files[key].new.append(new_text)

def add_previous_display(key):
    length = len(files[key].display)
    if length > 1:
        prev = files[key].display[length - 1]
    else:
        prev = True
    files[key].display.append(prev)

def remove_files(pattern):
    for key in files:
        if pattern in files[key].new[-1]:
            files[key].display.append(False) # manually adding false to the display list
            files[key].new.append(files[key].new[-1])
        else: 
            files[key].new.append(files[key].new[-1])
            add_previous_display(key) # calling this to make sure the previous value of display is set

def rename_files():
    """Applies all the changes the user has input in loop() to the files
       Once this is called, the changes are final.
    """
    for elem in files.values():
        # if the top of the stack display is True
        if elem.display[-1]:
            print(f"Renaming {elem.original} to {elem.new[-1]}")
            old = os.path.join(elem.path, elem.original)
            new = os.path.join(elem.path, elem.new[-1])
            os.rename(old, new)
    exit()

def cleanup():
    """Replaces double spaces with single spaces 5 times
       Removes all periods except extension period
    """
    replace_str(".", "")
    for i in range(5):
        replace_str("  ", " ")


def get_option(resp):
    """Applies the appropriate action based on the users input in loop()

       Parameter:
       resp -- string of the users input
    """

    splt = shlex.split(resp) # arguments split
    if len(splt) < 1:
        print("Not enough arguments given")
        return
    resp_lower = resp.lower()
    first_arg = splt[0].lower()
    print(first_arg)
    if first_arg == "replace":
        if len(splt) <= 1:
            print("Not enough arguments for replace utility")
            return
        elif len(splt) == 2:
            new = ""
        elif len(splt) >= 3:
            new = splt[2]
        old = splt[1]
        replace_str(old, new)
        
    elif first_arg == "range":
        if len(splt) <= 3:
            print("Not enough arguments for range_replace utility")
            return
        elif len(splt) == 4:
            new = ""
        elif len(splt) >= 5:
            new = splt[4]
        old = splt[3]
        min_r, max_r = splt[1], splt[2]
        range_replace(min_r, max_r , old, new)

    elif first_arg == "front":
        if len(splt) < 2:
            print("Not enough arguments for front utility")
            return
        try:
            n = int(splt[1])
        except ValueError:
            print(f"{splt[1]} is not a valid integer argument")
            return
        remove_from_front(n)

    elif first_arg == "mid":
        if len(splt) < 3:
            print("Not enough arguments for mid utility")
            return
        try:
            left = int(splt[1])
            right = int(splt[2])
        except ValueError:
            print("Not valid integer arguments")
            return
            
        remove_from_middle(left, right)


    elif first_arg == "end":
        if len(splt) < 2:
            print("Not enough arguments for end utility")
            return
        try:
            n = int(splt[1])
        except ValueError:
            print(f"{splt[1]} is not a valid integer argument")
            return
        remove_from_end(n)

    elif first_arg == "insert":
        if len(splt) < 3:
            print("Not enough arguments for insert utility")
            return
        try:
            position = int(splt[1])
        except ValueError:
            print("Not valid integer argument")
            return
        text = splt[2]
        insert_text(position, text)

    elif first_arg == "cleanup":
        cleanup()

    elif first_arg == "undo":
        undo()
    
    elif first_arg == "hide":
        global HIDE
        HIDE = not HIDE # flips the value of hide

    elif first_arg == "remove":
        if len(splt) < 2:
            print("Not enough arguments given for remove utility")
            return
        pattern = splt[1]
        remove_files(pattern)

    elif first_arg == "rename":
        rename_files()

    elif first_arg == "exit":
        exit()

    return



def loop():
    """Loops until the user inputs "exit" or "rename"
       Asks them to input what changes to the files
    """
    while True:
        print_current()
        if not HIDE:
            print("\n\nInput Commands\n---------------------")
            print("replace str_old str_new\t\t: takes in two strings and replaces all occurences of the old string with the new string")
            print("range min max str_old str_new\t: replace utility but only works on a range of numbers. See README.md for more details")
            print("front n\t\t\t\t: removes the first n chars from the file")
            print("mid left right\t\t\t: removes the chars the left index to the right index the file")
            print("end n\t\t\t\t: removes the last n chars from the file")
            print("insert n text\t\t\t: inserts text at position n")
            print("cleanup\t\t\t\t: applies common fixes. Read documentation for specifics")
            print("undo\t\t\t\t: un applies your last change")
            print("hide\t\t\t\t: toggles if this list of commands should be shown")
            print("remove text\t\t\t: removes all files that follow the format of text")
            print("rename\t\t\t\t: applies all the changes to the actual files")
            print("exit\t\t\t\t: exits the program\n")
        else:
            print("Input your Command\n---------------------")
        get_option(input())




def main():
    """Main function
    """

    if len(sys.argv) < 2:
        print("No Directory given in argument")
        exit()

    # arguments 2 through n are the file extensions the script will use
    if len(sys.argv) >= 3:
        global EXTENSIONS
        EXTENSIONS = []
        for i in range(2, len(sys.argv)):
            print(f"ARG is {sys.argv[i]}")
            if '*' in sys.argv[i]:
                global ALL_FILES
                ALL_FILES = True
                break
            EXTENSIONS.append(sys.argv[i])


    global DIR
    # 1st argument is the directory this script works on
    DIR = sys.argv[1]

    # addes files to files{}
    for filename in os.listdir(DIR):
        f = os.path.join(DIR, filename)
        # if boolean is True, we are adding every file in DIR
        if ALL_FILES:
            ext = os.path.splitext(filename)[1] # filename extension
            files[filename] = file_struct(filename, DIR, ext)
        else:
            # checking if it is a file
            for ext in EXTENSIONS:
                if f.endswith(ext):
                    files[filename] = file_struct(filename, DIR, ext)

    if len(files) > 0:
        print()
        loop()
    else:
        print(f"No files with extension {EXTENSIONS} found\nPick a new directory or read the README.md for how to change which extensions are used")

if __name__ == "__main__":
    main()
