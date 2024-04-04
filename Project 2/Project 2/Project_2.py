# Tyler Cunanan | comp 467 | fall 2023
from distutils.command.check import check
import pandas as pd
import pymongo, sys, argparse
from argparse import ArgumentParser, FileType
from datetime import datetime, date

def _parseDate(num):
    pDay = num[6:8]
    pMonth = num[4:6]
    pYear = num[0:4]
    date_given = pMonth + '-' + pDay + '-' + pYear
    if args.Verbose: print("Date Parced")
    return date_given

## ArgParse ##

parser = ArgumentParser()

parser.add_argument('-f', dest='workFiles', nargs='+')
parser.add_argument("-x", "--Xytech", help="Xytech file input")
parser.add_argument("-o", "--Output", help="to CSV or Database. Use [CSV] or [DB]")
parser.add_argument("-v", "--Verbose", help="output becomes more verbose", action="store_true")

# if args.Verbose: print("") (verbose insert)

args = parser.parse_args()

if args.workFiles is None:
    print("No BL/Flames files selected")
    sys.exit(2)
else:
    jobs = args.workFiles

if args.Xytech is None:
    print("No Xytech files selected")
    sys.exit(2)
else:
    wOrder = args.Xytech

if args.Xytech is None:
    print("No selection of CSV or Database")
    sys.exit(2)
else:
    fileOut = args.Output
    if fileOut == 'CSV' and fileOut == 'DB':
        msg = "'" + fileOut + "' Is not a valid input"
        print(msg)
        sys.exit(2)

print("Program active")
if args.Verbose: print("verbose!")

## read Xytech ##

f = open(wOrder, 'r')
fileXytech = f.read()
fileXytech = fileXytech.split("\n")
fileXytech[:] = (value for value in fileXytech if value != '')
f.close()
if args.Verbose: print("Xytech file Imported")

i = fileXytech.index("Location:") + 1
j = fileXytech.index("Notes:")

for line in fileXytech:
    if "Producer" in line:
        producer = line
    if "Operator" in line:
        operator = line
    if "Job" in line:
        job = line

note = fileXytech[j+1]

top = []

top.append(producer.replace("Producer: ", ''))
top.append(operator.replace("Operator: ", ''))
top.append(job.replace("Job: ", ''))
top.append(note)
if args.Verbose: print("Grabing details")

checks = []
while i < j:
    if 'Avatar' in fileXytech[i]:
        temp = fileXytech[i].split("Avatar")
        checks.append(temp)
    i += 1
if args.Verbose: print("Xytech has been parced")

i = 0
while i < len(checks):
    checks[i][1] = "Avatar"+checks[i][1]
    i += 1

## Import Files ##

#pathImport = "C:\Users\User\Documents\College_codeing\Project 2\import_files"

fileBase = []
extracted = []
for x in jobs:
    temp = str(x).replace("'",'')
    extracted.append(temp)

count = 1
for fJob in extracted:
    f = open(fJob, 'r')
    info = f.read()
    lines = info.split("\n")
    lines.sort()
    lines[:] = (value for value in lines if value != '')
    temp = fJob.split(".")
    names = temp[0].split("_")
    fName = names[1]
    msg = fJob + " Imported"
    if args.Verbose: print(msg)
    dated = _parseDate(names[2])
    data = []
    if names[0] == "Baselight":
        for x in lines:
            temp = x.split("Avatar")
            temp = "Avatar"+temp[1]
            fileBase.append(temp)
            tag = "Baselight"
    else:
        for x in lines:
            temp = x.split(" ",1)
            fileBase.append(temp[1])
            tag = "Flame"
    f.close()

    fileBase.sort()

    if args.Verbose: print("{} have been imported".format(fJob))

    ## File Parcer ##

    i = 0
    j = len(fileBase)
    tempStep = []
    while i < j:
        tempStep.append(fileBase[i].split(" ", 1))
        i += 1
    if args.Verbose: print("Spliting Frames and files")

    i = 1
    k = 0
    flist = []
    nlist = []
    flist.append(tempStep[0][0])
    ntemptemp = tempStep[0][1].split(" ")
    ntemp = []
    for x in ntemptemp:
        ntemp.append(int(x))

    while i < j:
        if tempStep[i][0] == flist[k]:
            ntemptemp = tempStep[i][1].split(" ")
            for x in ntemptemp:
                if x != '<null>' and x != '<err>': ntemp.append(int(x))
        else:
            ntemp.sort()
            nlist.append(ntemp)
            ntemptemp = []
            ntemp = []
            ntemptemp = tempStep[i][1].split(" ")
            for x in ntemptemp:
                if x != '':
                    if x != '<null>' and x != '<err>': ntemp.append(int(x))
            flist.append(tempStep[i][0])
            k += 1
        i += 1
    ntemp.sort()
    nlist.append(ntemp)
    if args.Verbose: print("Files Compacted")

    fileLen = len(flist)

    i = 0
    j = 0
    while i < fileLen:
        while j < len(checks):
            if flist[i] in checks[j][1]:
                msg = checks[j][0] + flist[i]
            j += 1
        flist[i] = msg
        j = 0
        i += 1
    if args.Verbose: print("File paths re-written")

    ## Num Parce ##

    parced = []
    holdlist = []
    start = 0
    end = 0
    i = 0
    while i < fileLen:
        j = len(nlist[i])
        temp = nlist[i]
        start = temp[0]
        end = temp[0]
        size = 1
        ii = 1
        while ii < j:
            if temp[ii] - temp[ii-1] == 1:
                end = temp[ii]
            else:
                if start == end:
                    holdlist.append(str(start))
                else:
                    msg = str(start) + '-' + str(end)
                    holdlist.append(msg)
                start = temp[ii]
                end = temp[ii]
            ii += 1
        if start == end:
            holdlist.append(str(start))
        else:
            msg = str(start) + '-' + str(end)
            holdlist.append(msg)
        parced.append(holdlist)
        holdlist = []
        # if args.Verbose: print("{} of {} frame strings parced".format(i,fileLen))
        i += 1

    if args.Verbose: print("Frames prossessed")

    ## import files into Database/CSV ## 

    today = date.today()
    myScriptDict = []
    myFileDict = []
    temp = wOrder.split(".")
    temp = temp[0].split("_")
    dateStamp = _parseDate(temp[1])
    cvsDate = temp[1]

    if fileOut == 'DB':
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        if args.Verbose: print("Opening Database")

        i = 0
        j = 0
        hold = []
        frames = []
        while i < fileLen:
            temp = parced[i]
            myScriptDict.append({"User":top[1], "Machine":tag, "OnFile":fName, "DateFile":dateStamp,"submit":str(today)})
            j = 0
            while j < len(temp):
                myFileDict.append({"OnFile":fName, "DateFile":dateStamp,"Location":flist[i],"Frames":temp[j]})
                j += 1
            i += 1
            # if args.Verbose: print("{} of {} {}'s sets".format(i,fileLen,fJob))
            

        mydb = myclient["Project_2_Database"]
        mycol1 = mydb["Script"]
        mycol1.insert_many(myScriptDict)
        
        mycol2 = mydb["Files"]
        mycol2.insert_many(myFileDict)
        if args.Verbose: print("Files added to the Database")

    else: #commented out to get CSV and DB filled

        if args.Verbose: print("Prepping CSV")
        i = 0
        j = 0
        hold = []
        frames = []
        while i < fileLen:
            temp = parced[i]
            j = 0
            while j < len(temp):
                hold.append(flist[i])
                hold.append('')
                hold.append(temp[j])
                hold.append('')
                frames.append(hold)
                j += 1
                hold = []
            i += 1
            # if args.Verbose: print("{} of {} {}'s CVS done".format(i,fileLen,fJob))

        export = pd.DataFrame(frames, columns = top)
        export.to_csv(r'C:\Users\User\Documents\College_codeing\Project 2\export_{}_{}.csv'.format(count, cvsDate), index=False)
        count += 1
        if args.Verbose: print("CSV explorted")
