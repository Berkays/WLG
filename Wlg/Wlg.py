#Wordlist Generator

#usage wlg.py min-len max-len --type 1-9 -o [Options] -f filename.txt

#Ex. wlg.py 4 8 --type 1 -o charset 12345 prefix test -f file.txt
#Outputs test[1111-5555]

#options
# 1 - Uppercase
# 2 - With Reverse
# 3 - Prefix
# 4 - Suffix
# 5 - charset
# 7 - Pattern use @ character
# 6 - year-range
#types
# 1 - Alphanumeric (charset,uppercase,reverse,prefix,suffix)
# 2 - Calendar (prefix,suffix)
# 3 - Pattern

import argparse
import os.path
import sys
from random import randint
from itertools import product

def Alphanumeric():
    global lineCount
    List = []
    c = getValue("charset")
    if(c is -1):
        print("Need to specify charset")
        return
    
    for i in range(args.minLength,args.maxLength + 1):
        permutationList = product(args.options[c],repeat=i)
        for entry in permutationList:
            line = "".join(entry) + "\n"      
            List.append(line)           
            lineCount = lineCount + 1

    applyOptions(List)
    return List

def Dates():
    global lineCount
    List = []

    minyear = 1800
    maxyear = 2200
    t1 = getValue("min-year")
    t2 = getValue("max-year")
    if(t1 is not -1):
        try:
            val = int(args.options[t1])
            minyear = val
        except ValueError as e:
            print("Value Error")
    if(t2 is not -1):
        try:
            val = int(args.options[t2])
            maxyear = val
        except ValueError as e:
            print("Value Error")

    print("Starting year - {}".format(minyear))
    print("Ending year - {}".format(maxyear))
    
    for p1 in range(0,32):
        for p2 in range(0,13):
            for p3 in range(minyear,maxyear + 1):
                line = ""
                rline = ""
                if p1 < 10:
                    line += '0' + str(p1)
                    rline += '0' + str(p1)
                else:
                    line += str(p1)
                    rline += str(p1)
                if p2 < 10:
                    line += '0' + str(p2)
                    rline = '0' + str(p2) + rline
                else:
                    line += str(p2)
                    rline = '0' + str(p2) + rline
                line += str(p3) + '\n'
                rline = str(p3) + rline + '\n'
                List.append(line)
                List.append(rline)
                lineCount = lineCount + 2

    applyOptions(List)
    return List

def Pattern():
    global lineCount
    List = []
    c = getValue("charset")
    if(c is -1):
        print("Need to specify charset")
        return
    p = getValue("pattern")
    if(p is -1):
        print("Need to specify pattern")
        return

    #Number of characers to replace
    permutationLen = args.options[p].count('@')
    #List of indexes to replace
    indexList = []
    for i in range(0,len(args.options[p])):
        if(args.options[p][i] == '@'):
            indexList.append(i)

    if(len(indexList) == 0):
        print("Nothing to replace")
        return

    str = list(args.options[p])
    perms = product(args.options[c],repeat=permutationLen)
    for entry in perms:
        line = "".join(entry) + "\n"
        for index,i in zip(indexList,range(len(line))):
            str[index] = line[i]
        List.append("".join(str) + "\n")
        lineCount = lineCount + 1

    applyOptions(List)
    return List

def ImportFile():
    global lineCount
    List = []
    c = getValue("charset")
    if(c is -1):
        print("Need to specify charset")
        return
    im = getValue("import")
    if(im is -1):
        print("Need to specify import file")
        return
   
    file = open(args.options[im],mode='r')
    imported = []
    for line in file:
        if(len(line) <= 3):
            continue
        imported.append(line)
    if(len(imported) == 0):
        print("Empty import file")
        return

    for file_entry in imported:
        offset = max(0,args.minLength - len(file_entry))
        for i in range(offset,args.maxLength + 1):
            permutationList = product(args.options[c],repeat=i)
            for entry in permutationList:
                line = file_entry.rstrip("\n") + "".join(entry) + "\n"      
                List.append(line)           
                lineCount = lineCount + 1

    applyOptions(List)
    return List

def getValue(search):
    if(args.options is None):
        return -1
    for i in range(0,len(args.options)):
        if(args.options[i] == search):
            return i + 1
    return -1

def applyOptions(List):
    print("\nOptions\n--------")
    p = getValue("prefix")
    s = getValue("suffix")
    u = getValue("upper")
    r = getValue("reverse")
    if(p is not -1):
        print("Prefix : {}".format(args.options[p]))
        for i in range(0,len(List)):
            List[i] = args.options[p] + List[i]
    if(s is not -1):
        print("Suffix : {}".format(args.options[s]))
        for i in range(0,len(List)):
            List[i] = List[i] + args.options[s]
    if(u is not -1 and args.options[u] is "1"):
        print("Uppercase")
        for i in range(0,len(List)):
            List[i] = List[i].upper()
    if(r is not -1 and args.options[r] is "1"):
        print("Reverse")
        for i in range(0,len(List)):
            List[i] = List[i][::-1]

def generate():
    if(args.type == 1):
        return Alphanumeric()
    elif(args.type == 2):
        return Dates()
    elif(args.type == 3):
        return Pattern()
    elif(args.type == 4):
        return ImportFile()
    elif(args.type == 5):
        return PhoneNumbers()
    else:
        print("Invalid wordlist type")
        return 0

parser = argparse.ArgumentParser(description="WordList Generator")
parser.add_argument("--min",type=int,default=8,dest = "minLength",help="Minimum number of characters to add (Prefix excluded)")
parser.add_argument("--max",type=int,default=9,dest = "maxLength",help="Maximum number of characters to add (Prefix excluded)")
parser.add_argument("-t","--type",type=int,required=True,dest = "type",help="Type of wordlist to produce")
parser.add_argument("-o","--options",type=str,nargs='+',help="Options to use with wordlist")
parser.add_argument("-f","--file",type=str,default="none",dest="filename",help="The file to write")
args = parser.parse_args()

print("\nWordlist Generator v1.0 - berkaygursoy@gmail.com")
for i in range(100):
    print('-',end='')
print("\n")

if(os.path.exists(args.filename) == True):
    args.filename = "wordlist-{}.txt".format(randint(10000,99999))
    print("File exists. Generating random name...({})".format(args.filename))
if(args.filename == "none"):
    args.filename = "wordlist-{}.txt".format(randint(10000,99999))
    print("File name not specified. Generating random name...({})".format(args.filename))
if(args.maxLength <= args.minLength):
    print("Maximum length cannot be lower than minimum length")
    args.maxLength = args.minLength

lineCount = 0

generatedList = generate()

if(lineCount == 0):
    print('\nNothing generated')
    sys.exit()

file = open(args.filename,mode="w")
for entry in generatedList:
    file.write(entry)

print("\n{} Lines written into {}".format(lineCount,args.filename))
file.close()


