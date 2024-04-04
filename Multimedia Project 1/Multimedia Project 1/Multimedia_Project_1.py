from tkinter.tix import FileSelectBox
import pandas as pd
from cmath import inf
from operator import index
import fileinput
import string

# if verbose: print("")

#################
## FILE IMPORT ##
#################

f = open('Baselight_export.txt', 'r')
fileBaselight = f.read()
fileBaselight = fileBaselight.replace(" <null>", "")
fileBaselight = fileBaselight.replace(" <err>", "")
fileBaselight = fileBaselight.split("\n")
fileBaselight[:] = (value for value in fileBaselight if value != '')
f.close()

f = open('Xytech.txt', 'r')
fileXytech = f.read()
fileXytech = fileXytech.split("\n")
fileXytech[:] = (value for value in fileXytech if value != '')
f.close()

i = fileXytech.index("Location:") + 1
j = fileXytech.index("Notes:")

names = ["Producer", "Operator", "Job"]

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

#################
## READ Xytech ##
#################

checks = []

while i < j:
    checks.append(fileXytech[i].split("Barbie"))
    i += 1

fileBaselight.sort()
#for x in fileBaselight:
#    print(x)

i = 0
j = len(fileBaselight)
tempStep = []
while i < j:
    tempStep.append(fileBaselight[i].split(" ", 1))
    i += 1

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
            ntemp.append(int(x))
    else:
        ntemp.sort()
        nlist.append(ntemp)
        ntemptemp = []
        ntemp = []
        ntemptemp = tempStep[i][1].split(" ")
        for x in ntemptemp:
            if x != '':
                ntemp.append(int(x))
        flist.append(tempStep[i][0])
        k += 1
    i += 1
ntemp.sort()
nlist.append(ntemp)

################
##  RE-WRITE  ##
## FILE NAMES ##
################

fileLen = len(flist)
toReplace = []
for x in flist:
    toReplace.append(x.split("Barbie"))

i = 0
j = 0
while i < fileLen:
    while j < len(checks):
        if toReplace[i][1] == checks[j][1]:
            toReplace[i][0] = checks[j][0]
        j += 1
    msg = toReplace[i][0]+"Barbie"+toReplace[i][1]
    flist[i] = msg
    j = 0
    i += 1

#for x in flist:
#    print(x)

####################
## NUMBER PARSING ##
####################

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
    i += 1

for x in parced:
    print(x)

################
## WRITE MODE ##
################

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

export = pd.DataFrame(frames, columns = top)

export.to_csv(r'C:\Users\User\Documents\College_codeing\Multimedia Project 1\Multimedia Project 1\export.csv', index=False)

