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

- replace str_old str_new   		: takes in two strings and replaces all occurences of <b>str_old</b> with <b>str_new</b>
- range min max str_old str_new     	: similar to replace, but only does the replace on files that contains integers inclusively between [<b>min</b>, <b>max</b>]
- front n   				: removes the first <b>n</b> chars from the file
- mid left right       			: takes in two integers, <b>left right </b>, and removes all text inside the range of [left,right]
- end n     				: removes the last n chars from the file excluding extension
- insert n text    			: inserts string <b>text</b> at position <b>n</b>. Userful for appending text to the front with position 0 or appending to the end with position -1
- cleanup   				: applies common fixes such as removes periods and replacing double spaces with single spaces
- undo      				: un does the last change applies
- hide      				: hides the list of commands if you just want to see the current iteration of files
- remove text   			: removes all files from the change stack that contain string <b>text</b>
- rename    				: <b>FINAL</b> command to applies changes. No files are renamed until this command is input
- exit      				: exits the program with no changes applies  

## Examples

# Contact

Nolan Winsman - [@Github](https://github.com/nolanwinsman) - nolanwinsman@gmail.com

Project Link: [https://github.com/nolanwinsman/bulk_renamer](https://github.com/nolanwinsman/bulk_renamer)

# Contributers
- nolanwinsman

## Files

- bulk_renamer.py : utility to rename multiple files to users specifications
- README.md : this file

