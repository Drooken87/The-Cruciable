
from base64 import decode
from io import BytesIO
import os, string
import pymongo, sys, argparse, subprocess, xlsxwriter, csv, shlex
import pandas as pd
from frameioclient import FrameioClient
from argparse import ArgumentParser
from datetime import date

# Keep It Stupid Idiot

# subprocess.run("ffmpeg -ss 5 -i \"C:\\Users\\User\\Documents\\College_codeing\\Project 3\\Project 3\\twitch_nft_demo.mp4\" -frames:v 1 -vf \"scale=96:74\" TestShot2.png")

# time code #
def _frameConvert(frames):
    _frames = int(frames)
    tFrame = "00"
    tSeconds = "00"
    tMinutes = "00"
    tHours = "00"
    FPS = 60

    if _frames > FPS:
        tFrame = str(int(((_frames % FPS) / FPS) * 100))
        _frames = int(_frames/FPS)
    else:
        tFrame = str(int(((_frames % FPS) / FPS) * 100))
        _frames = "00"
    if len(tFrame) == 1:
            tFrame = "0" + tFrame

    if _frames != "00" and _frames > 60:
        tSeconds = str(_frames % 60)
        _frames = int(_frames/60)
    else:
        tSeconds = str(_frames)
        _frames = "00"
    if len(tSeconds) == 1:
            tSeconds = "0" + tSeconds

    if _frames != "00" and _frames > 60:
        tMinutes = str(_frames % 60)
        _frames = int(_frames/60)
    else:
        tMinutes = str(_frames)
        _frames = "00"
    if len(tMinutes) == 1:
            tMinutes = "0" + tMinutes

    if _frames != "00":
        tHours = str(_frames)
    if len(tHours) == 1:
            tHours = "0" + tHours

    timecode = "{}:{}:{}.{}".format(tHours,tMinutes,tSeconds,tFrame)
    return timecode
# time codes #

# --prossess, --output

parser = ArgumentParser()

parser.add_argument("-p", "--Process", help="Prosses a video")
parser.add_argument("-o", "--Output", help="to a XLS CVS or DB")
parser.add_argument("-v", "--Verbose", help="output becomes more verbose", action="store_true")

args = parser.parse_args()

if args.Process is None:
    print("No Video selected")
    sys.exit(2)
else:
    video = args.Process
    temp = video.split('.')
    if temp[1] != "mp4":
        print("invalid video type")
        sys.exit(2)

if args.Output is None:
    print("No Output selected")
    sys.exit(2)
else:
    XLSoutput = args.Output
    if XLSoutput == 'CSV' and XLSoutput == 'DB' and XLSoutput == 'XLS':
        print("'{}' Is not a valid input".format(XLSoutput))
        sys.exit(2)

# duration: 00:01:39.63 -> frames


#video = args.Process
#video = "twitch_nft_demo.mp4"

txt = "ffmpeg -i {} -hide_banner".format(video)
process = subprocess.Popen(shlex.split(txt), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
durration = 0
for x in process.stdout.readlines():
    decoded = x.decode()
    if(decoded.startswith('  Duration:')):
        durration = decoded.strip().split(",")[0].strip().split(" ")[1]

vidLength = durration
timeS = vidLength.split(':')
hour = int(timeS[0])
mins = int(timeS[1])
temp = timeS[2].split(".")
seconds = int(temp[0])
frames = int((int(temp[1])/100)*60)
vidFrames = (hour*60*60*60) + (mins*60*60) + (seconds*60) + frames

if args.Verbose: print("Video inported")

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Project_2_Database"]
mycol2 = mydb["Files"]
mydoc = mycol2.find()
fnames = []
fpath = []

for x in mydoc:
    temp = x.values()
    temp2 = []
    for y in temp:
        temp2.append(y)
    fnames.append(temp2[4]) #populate with frames. filter frames out below the threshhold
    fpath.append(temp2[3])

if args.Verbose: print("Database called")

if XLSoutput == 'DB':
    # pretend there's Database code here. #
    #  Should put more than this but it   #
    #         was all in project 2        #
    if args.Verbose: print("Database prossessing")
    sys.exit(2)
elif XLSoutput == 'CVS':
    CVSout = []
    top = ["Scene Job","Frame Range"]
    i = 0
    while i < len(fnames):
        temp = []
        temp.append(fpath[i])
        temp.append(fnames[i])
        CVSout.append(temp)
        i += 1
    export = pd.DataFrame(CVSout, columns = top)
    cvsDate = date.today()
    export.to_csv(r'C:\Users\User\Documents\College_codeing\Project 3\export_{}.csv'.format(cvsDate), index=False)
    # Pretend there's CSV code here
    if args.Verbose: print("CVS prossessing")
    sys.exit(2)
else:
    if args.Verbose: print("Frames collected")
    # subprosses is fine. prossess = subprosses 31 min mark

    # find length of video and FPS
    # convert into frames. Query all frams that fall under that mark

    # frames doesnt matter, long as we know if it's the middle frame
    timeCollem = []
    tumbcollect = []
    pathcollect = []
    framecollect = []
    i = 0
    while i < len(fnames):
        temp = fnames[i]
        if '-' in temp:
            temp2 = temp.split('-')
            mid = int((int(temp2[1]) + int(temp2[0]))/2)
            timetemp = _frameConvert(temp2[0]) + '-' + _frameConvert(temp2[1])
            time = _frameConvert(mid)
        else:
            mid = int(temp)
            timetemp = _frameConvert(mid)
            time = _frameConvert(mid)

        if mid < vidFrames:
            timeCollem.append(timetemp)
            tumbcollect.append(time)
            pathcollect.append(fpath[i])
            framecollect.append(temp)
    
        i += 1
    if args.Verbose: print("Frames converted to Time Codes")
    # from a range, find the middle, and extract that
    # add as a new collem
    # 96x74 thumbnail

    

    i = 0
    while i < len(tumbcollect):
        txt = "ffmpeg -ss {} -i {} -hide_banner -frames:v 1 -vf \"scale=96:74\" TMBN-{}.png".format(tumbcollect[i],video,i)
        subprocess.run(txt)
        i += 1

    #if args.Verbose: print("Thumbnails saved")

    EXLtxt = "Thumnails.xlsx"

    #thumbname = r'C:\Users\User\Documents\College_codeing\Project 3\Project 3\TestShot.png'

    #file = open(thumbname, 'rb')
    #data = BytesIO(file.read())
    #file.close()

    workbook = xlsxwriter.Workbook(EXLtxt)
    worksheet = workbook.add_worksheet()
    i = 1
    worksheet.write(0, 0, "Scene Job")
    worksheet.write(0, 1, "Frame Range")
    worksheet.write(0, 2, "Time Codes")
    worksheet.write(0, 3, "Thumbnails")
    while i < len(timeCollem)+1:
        worksheet.write(i, 0, pathcollect[i-1])
        worksheet.write(i, 1, framecollect[i-1])
        worksheet.write(i, 2, timeCollem[i-1])
    
        thumbname = r'C:\Users\User\Documents\College_codeing\Project 3\Project 3\TMBN-{}.png'.format(i-1)
        file = open(thumbname, 'rb')
        data = BytesIO(file.read())
        file.close()

        worksheet.insert_image(i, 3, thumbname, {'image_data': data})
        i += 1
        #upload thumbnail to frames.io later

    workbook.close()
    if args.Verbose: print("EXL file created")
    
    # Token: fio-u-0KoMJI_fGiFcxqWvEwJkmIBA5F1vWwPexWvkR586RoWwpDARrg_igy0xGDI6_VeW
    

    MyToken = "fio-u-0KoMJI_fGiFcxqWvEwJkmIBA5F1vWwPexWvkR586RoWwpDARrg_igy0xGDI6_VeW"

    client = FrameioClient(MyToken)
    me = client.users.get_me()


    destination_id = "9e154943-0638-49d5-bc62-69a14906f495"

    i = 0
    while i < len(timeCollem):
        asset = client.assets.create(
            parent_asset_id="1234abcd",
            name="TMBN-{}.png".format(i),
            type="file",
            filetype="image/png",
            filesize=os.path.getsize("TMBN-{}.png".format(i))
        )
        client.assets.upload(destination_id, "C:\\Users\\User\\Documents\\College_codeing\\Project 3\\Project 3\\TMBN-{}.png".format(i))
        if i % 10 == 1:
            print(i)
        if i > 200:
            sys.exit(2)
        i += 1

    client = FrameioClient(MyToken)
    me = client.users.get_me()

    if args.Verbose: print("Files Uploaded to Frame.IO")

# Thank you for everything Chaja. May of been a derp but you're by far my favorite teacher 
# Wished I could of tackled API, Couldnt get it to work when trying with google map API