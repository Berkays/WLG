# Wlg
Simple wordlist generator written in Python

Use with 64 bit python interpreter to avoid memory overflows.

#Usage

wlg.py min-len max-len --type 1-9 -o [Options] -f filename.txt

#Example

wlg.py 4 8 --type 1 -o charset 12345 prefix test -f file.txt

Outputs test[1111-5555]

#Options
 1 - Uppercase
 
 2 - With Reverse
 
 3 - Prefix
 
 4 - Suffix
 
 5 - charset
 
 7 - Pattern use @ character
 
 6 - year-range
 
#Types
 1 - Alphanumeric (charset,uppercase,reverse,prefix,suffix)
 
 2 - Calendar (prefix,suffix)
 
 3 - Pattern
 
