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

# If this is true, the user is not shown the availible utilities
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

def apply_function_all_files(fnc, *args):
    """Loops through all the elements in files{}
       and calls a function on them
    """
    for elem in files.values():
        fnc(elem, *args)

def replace_str(elem, old, new):
    """ Replaces the old string with the new string

    Parameters :
    old -- string to be replaced
    new -- string that replaces old
    """
    temp = elem.new[-1]
    temp = temp.replace(elem.ext, "") # removes the extension so that the replace will not affect it
    temp = temp.replace(old, new) # replaces old string with new string
    temp = f"{temp}{elem.ext}" # adds back the extension
    add_new(elem, temp)

def range_replace(elem, min_r, max_r, old, new):
    min_r, max_r = int(min_r), int(max_r)
    # if the min value is greater than the max value, swaps the values
    if min_r > max_r:
        min_r, max_r = max_r, min_r

    if min_r < 0 or max_r < 0:
        print("Invalid arguments")
        return

    temp = elem.new[-1]
    try:
        num = int(re.search(r'\d+', temp).group()) # attempts to find a number
    except Exception as e:
        print(f"Exception {e} occured")

    if num >= min_r and num <= max_r:
        temp = temp.replace(elem.ext, "") # removes the extension so that the replace will not affect it
        temp = temp.replace(old, new) # replaces old string with new string
        print(f"if statement temp: \n{temp}\nNEW: {new}")
        temp = f"{temp}{elem.ext}" # adds back the extension
        add_new(elem, temp)
    else:
        add_new(elem, elem.new[-1])

def remove_from_end(elem, n):
    """Removes the last n chars (excluding the extension) from the files in files{}
    """
    temp = elem.new[-1]
    print(f"EXT\t{elem.ext}")
    # removes last n characters from string except for the extension
    temp = temp.replace(elem.ext, "")
    length = len(temp) - n
    add_new(elem, f"{temp[:length]}{elem.ext}")

def remove_from_middle(elem, left, right):
    temp = elem.new[-1]
    temp = temp.replace(elem.ext, "") # removes the extension so that the replace will not affect it
    add_new(elem, f"{temp[:left]}{temp[right:]}{elem.ext}")

def remove_from_front(elem, n):
    """ Removes the first n chars from the files in files{}
    """
    temp = elem.new[-1]
    temp = temp.replace(elem.ext, "")
    # removes first n characters from string
    add_new(elem, f"{temp[n:]}{elem.ext}")

def clear_screen():
    return
    #os.system('cls' if os.name == 'nt' else 'clear')

def print_current():
    """Prints what the files will be renamed to if rename_files() is called
    """
    clear_screen()
    print("-----Current Iteration of Changes-----")
    for elem in files.values():
        if elem.display[-1]:
            print(elem.new[-1])

def insert_text(elem, position, text):
    temp = elem.new[-1]
    temp = temp.replace(elem.ext, "") # removes the extension so that the insert will not affect it
    # edge case to add text to the end
    if position <= -1:
        add_new(elem, f"{temp}{text}{elem.ext}")
    else:
        add_new(elem, f"{temp[:position]}{text}{temp[position:]}{elem.ext}")

def undo(elem):
    """ Redacts the last change the user input in loop()
    """
    assert len(elem.new) == len(elem.display)
    if len(elem.new) > 1:
        elem.new.pop()
        elem.display.pop()

def add_new(elem, new_text):
    length = len(elem.display)
    print(f"The new text: {new_text}")
    if length > 1:
        prev = elem.display[length - 1]
    else:
        prev = True
    elem.display.append(prev)
    elem.new.append(new_text)

def add_previous_display(elem):
    """Used to keep elem.display equal to what it was.
       So if elem.display was True on edit 6, it will be true on edit 7
       unless that edit is to change display to False
    """
    length = len(elem.display)
    if length > 1:
        prev = elem.display[length - 1]
    else:
        prev = True
    elem.display.append(prev)

def remove_file(elem, pattern):
    if pattern in elem.new[-1]:
        elem.display.append(False) # manually adding false to the display list
        elem.new.append(elem.new[-1])
    else: 
        elem.new.append(elem.new[-1])
        add_previous_display(elem) # calling this to make sure the previous value of display is set

def rename_file(elem):
    """Applies all the changes the user has input in loop() to the files
       Once this is called, the changes are final.
    """
    # if the top of the stack display is True
    if elem.display[-1]:
        old = os.path.join(elem.path, elem.original)
        new = os.path.join(elem.path, elem.new[-1])
        # if old == new, no need to rename
        if old != new:
            print(f"Renaming {elem.original} to {elem.new[-1]}")
            os.rename(old, new)

def add_empty_edit(elem):
    """Appends the last value of new to new
       This is used to make sure the length of new in file_struct is 
       always the same between elements
    """
    elem.new.append(elem.new[-1])

def add_parenthesis(elem):
    """TODO make this function work
    """
    print(f"Add Para being called on {elem.new[-1]}")
    numbers = []
    temp = ""
    for c in elem.new[-1]:
        if c.isdigit():
            temp += c
        elif not c.isdigit() and len(temp) > 0:
            numbers.append(temp)
            temp = ''
    for num in numbers:
        # four digit number found
        if len(num) == 4:
            replace_str(elem, num, f"({num})")
            return
    add_empty_edit(elem)

def cleanup():
    """Replaces double spaces with single spaces 5 times
       Removes all periods except extension period
    """
    apply_function_all_files(replace_str, ".", " ")
    for i in range(5):
        apply_function_all_files(replace_str, "  ", " ")
    # if there is a four digit number, add parenthesis around it.
    # this is useful for movie files with the year so Movie 1999.mkv would change to Movie (1999).mkv
    apply_function_all_files(add_parenthesis)
    # TODO make sure an undo() undoes all of this with one call

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
        apply_function_all_files(replace_str, old, new)
        
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
        apply_function_all_files(range_replace, min_r, max_r , old, new)

    elif first_arg == "front":
        if len(splt) < 2:
            print("Not enough arguments for front utility")
            return
        try:
            n = int(splt[1])
        except ValueError:
            print(f"{splt[1]} is not a valid integer argument")
            return
        apply_function_all_files(remove_from_front, n)

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
        apply_function_all_files(remove_from_middle, left, right)


    elif first_arg == "end":
        if len(splt) < 2:
            print("Not enough arguments for end utility")
            return
        try:
            n = int(splt[1])
        except ValueError:
            print(f"{splt[1]} is not a valid integer argument")
            return
        apply_function_all_files(remove_from_end, n)

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
        apply_function_all_files(insert_text, position, text)

    elif first_arg == "cleanup":
        cleanup()

    elif first_arg == "undo":
        apply_function_all_files(undo)
    
    elif first_arg == "hide":
        global HIDE
        HIDE = not HIDE # flips the value of hide

    elif first_arg == "remove":
        if len(splt) < 2:
            print("Not enough arguments given for remove utility")
            return
        pattern = splt[1]
        apply_function_all_files(remove_file, pattern)

    elif first_arg == "rename":
        apply_function_all_files(rename_file)
        exit()

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

    # adds files to files{}
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
