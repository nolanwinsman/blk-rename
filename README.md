### bulk_renamer

Python script to rename multiple files in a folder.


## Installation

1. Clone the repo
```sh
git clone https://github.com/nolanwinsman/bulk_renamer.git
```

## Getting Started

```sh
python bulk_renamer.py PATH_TO_DIRECTORY
```
- PATH_TO_DIRECTORY should be the absolute path to the directory you want to rename files inside of
- NOTE : you might need to do <b>sudo python...</b> if you get a permission error
- By default the script only works on video files ['.mp4', '.mkv', '.mov', '.avi']
If you want to use different file extensions, for example <b>.jpg</b> and <b>.png</b> instead, you can either change the global variable EXTENSIONS to <b>EXTENSIONS = ['.jpg', '.png']</b> at the top of bulk_renamer.py
or use the the CLI arguments 2 to n
```sh
python bulk_renamer.py PATH_TO_DIRECTORY .jpg .png
```

## Features

- replace   : takes in two strings and replaces all occurences of the first string with the second string
- range     : takes in two numbers for min and max
- front n   : removes the first n chars from the file
- mid       : takes in two integers, left right, and removes all text inside the range of (left,right)
- end n     : removes the last n chars from the file excluding extension
- insert    : takes in an integer and string for the position and text that is inserted. Userful for appending text to the front with position 0 or appending to the end with position -1
- cleanup   : applies common fixes such as removes periods and replacing double spaces with single spaces
- undo      : un does the last change applies
- hide      : hides the list of commands if you just want to see the current iteration of files
- remove    : TODO
- rename    : <b>FINAL</b> command to applies changes. No files are renamed until this command is input
- exit      : exits the program  

## Examples

# Contact

Nolan Winsman - [@Github](https://github.com/nolanwinsman) - nolanwinsman@gmail.com

Project Link: [https://github.com/nolanwinsman/bulk_renamer](https://github.com/nolanwinsman/bulk_renamer)

# Contributers
- nolanwinsman

## Files

- bulk_renamer.py : utility to rename multiple files to users specifications
- README.md : this file

