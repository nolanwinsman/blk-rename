### bulk_renamer

Python script to rename multiple files in a folder

## Getting Started

- python bulk_renamer.py PATH_TO_DIRECTORY
- PATH_TO_DIRECTORY should be the absolute path to the directory you want to rename files inside of
- NOTE : you might need to do <b>sudo python...</b> if you get a permission error


## Installation

1. Clone the repo
```sh
git clone https://github.com/nolanwinsman/bulk_renamer.git
```

## Features

- replace   : takes in two strings and replaces all occurences of the first string with the second string
- front n   : removes the first n chars from the file
- end n     : removes the last n chars from the file excluding extension
- cleanup   : applies common fixes such as removes periods and replacing double spaces with single spaces
- undo      : un does the last change applies
- rename    : final command to applies changes. No files are renamed until this command is input
- exit      : exits the program  

# Contact

Nolan Winsman - [@Github](https://github.com/nolanwinsman) - nolanwinsman@gmail.com

Project Link: [https://github.com/nolanwinsman/bulk_renamer](https://github.com/nolanwinsman/bulk_renamer)

# Contributers
- nolanwinsman

## Files

- bulk_renamer.py : utility to rename multiple files to users specifications
- README.md : this file

