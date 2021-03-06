from PIL import Image
import os, sys
import tkinter as tk
from datetime import date
import time

# Directions to different target folders
path = os.path.realpath("./")
inputPath = os.path.realpath("./")+"/originals/"
outputPath = os.path.realpath("./")+"/compressed/"
logPath = os.path.realpath("./")+"/files/log/"
imgList = os.listdir( inputPath )

# Date
today = date.today()
today = today.strftime("%d-%m-%y")
now = time.localtime()


def resize(q):
    current_time = time.strftime("%H:%M:%S", now)
    log = open(logPath+today+"_log["+current_time+"].txt", "w")
    errors, nr = [], 0
    for item in imgList:
        if os.path.isfile(inputPath+item):   
            if item.split(".")[-1]=="jpg":
                im = Image.open(inputPath+item)
                nr +=1
                imResize = im.resize(im.size, Image.ANTIALIAS)
                imResize.save(outputPath +item, 'JPEG', optimize=True, quality=q)
                oldSize, newSize = os.path.getsize (inputPath+item), os.path.getsize (outputPath+item)
                data = "\nFile: "+item+"\nSize: "+str(oldSize)+"\t NewSize: "+str(newSize)+"\t \nRatio:"+str(float((1-(newSize/oldSize))*100))[:4]+"%\n"
                log.write(data)
            elif(item.split(".")[-1]=="png"):
                im = Image.open(inputPath+item)
                nr +=1
                imResize = im.resize(im.size, Image.ANTIALIAS)
                imResize.save(outputPath +item, 'PNG', optimize=True, quality=q)
                oldSize, newSize = os.path.getsize (inputPath+item), os.path.getsize (outputPath+item)
                data = "\nFile:  "+item+"\nSize:  "+str(oldSize)+"\t NewSize:  "+str(newSize)+"\t \nRatio:"+str(float((1-(newSize/oldSize))*100))[:4]+"%\n"
                log.write(data)
            else:
                errors.append(item)
            prosenten = (str( (nr/(len(imgList)-len(errors)) * 100))+"%")
            print(prosenten+" \t Errors: "+str(len(errors))+" \t Success: "+str(nr))
    log.write("\n\n-------Errors--------\n")
    for error in errors:
        log.write(error+"\n")
    print("Log can be found at path: "+logPath)


def verifyInput(query):
    # Choose the quality number
    try:
        q = int(query)
        if q>0 and q<100:
            resize(q)
        else:
            print("Skriv et tall mellom 1 og 99 og press deretter enter")
    except ValueError as e:
        print(e) 
        print("Value not integer")



def fetch(entries):
    for entry in entries:
        field = entry[0]
        text  = entry[1].get()
        verifyInput(text) 



def makeform(root, fields):
    entries = []
    row = tk.Frame(root)
    lab = tk.Label(row, width=15, text=fields, anchor='w')
    ent = tk.Entry(row)
    row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
    lab.pack(side=tk.LEFT)
    ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
    entries.append(("Reduction", ent))
    return entries

if __name__ == '__main__':
    fields = 'Reduction number'
    root = tk.Tk()
    root.title("Imagen Compression") 
    root.iconphoto(True, tk.PhotoImage(file="./files/icon/acc.png"))
    l = tk.Label(root, text = "Compression of "+str(len(imgList))+" img") 
    l.config(font =("Courier", 14)) 
    l.pack()
    ents = makeform(root, fields)
    root.bind('<Return>', (lambda event, e=ents: fetch(e)))   
    b1 = tk.Button(root, text='Execute',
                  command=(lambda e=ents: fetch(e)))
    b1.pack(side=tk.LEFT, padx=5, pady=5)
    b2 = tk.Button(root, text='Quit', command=root.quit)
    b2.pack(side=tk.LEFT, padx=5, pady=5)
    root.mainloop()

