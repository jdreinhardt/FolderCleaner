import sys
import io
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import cleaner

def catchClose():
    outEntry.insert(END, "Nope. Sorry. Close main window to quit\n")

def helpDialog():
    messagebox.showinfo("Help", "This UI supports up to five folders in a batch.\n--VERBOSE will output all actions the script completes to the output window\n--SILENT will prevent any output from occuring\n--FILES ONLY will only process files, and will not delete any empty folders found\n--TEST ONLY will show all actions that will occur, but will not delete any files/foldersn\n--The number of days is set to determine the minimum time since the last modified date to qualify for deletion\n--PROCESS will process the job according to settings")

def aboutDialog():
    messagebox.showinfo("About", "Folder Cleaner UI v1.0\nUpdated Aug 2017")

def browseLocation(entry):
    dirPath = filedialog.askdirectory()
    entry.delete(0, END)
    entry.insert(0, dirPath)

def clearOutput():
    outEntry.delete(1.0, END)

def startProcess():
    allPaths = []
    args = []

    if ent1.get() != "":
        allPaths.append(ent1.get())
    if ent2.get() != "":
        allPaths.append(ent2.get())
    if ent3.get() != "":
        allPaths.append(ent3.get())
    if ent4.get() != "":
        allPaths.append(ent4.get())
    if ent5.get() != "":
        allPaths.append(ent5.get())

    for path in allPaths:
        args.append("-p")
        args.append(path)

    if filesVar.get() == True:
        args.append("-f")
    
    if verboseVar.get() == True:
        args.append("-v")

    if silentVar.get() == True:
        args.append("-s")

    if testonlyVar.get() == True:
        args.append("-t")

    args.append("-d")
    args.append(numericBox.get())

    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()

    output = cleaner.main(args)

    outEntry.insert(END, mystdout.getvalue())

    sys.stdout = old_stdout

root = Tk()
root.title("Folder Cleaner")
root.geometry("600x235")
root.resizable(False, False)

#Output Window generation
popup = Toplevel()
popup.title("Output")
popup.geometry("600x200")
popup.protocol('WM_DELETE_WINDOW', catchClose)

outClear = Button(popup, text="Clear", command=clearOutput)
outClear.pack(side=BOTTOM, fill=Y)
outEntry = Text(popup)
scroll = Scrollbar(popup)
scroll.pack(side=RIGHT,fill=Y)
outEntry.pack(fill=BOTH, expand=1)
scroll.config(command=outEntry.yview)
outEntry.config(yscrollcommand=scroll.set)

#Menus
menu = Menu(root)
root.config(menu=menu)

subMenu = Menu(menu)
menu.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Quit", command=root.destroy)

helpMenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpMenu)
helpMenu.add_command(label="Help", command=helpDialog)
helpMenu.add_separator()
helpMenu.add_command(label="About", command=aboutDialog)


#Main UI
frame = Frame(root)
frame.pack()

ent1 = Entry(frame, width=80)
ent1.grid(row=1, column=0, padx=5, pady=5, ipadx=2, ipady=2)
browse1 = Button(frame, text="Browse", command=lambda: browseLocation(ent1))
browse1.grid(row=1, column=1)

ent2 = Entry(frame, width=80)
ent2.grid(row=2, column=0, padx=5, pady=5, ipadx=2, ipady=2)
browse2 = Button(frame, text="Browse", command=lambda: browseLocation(ent2))
browse2.grid(row=2, column=1)

ent3 = Entry(frame, width=80)
ent3.grid(row=3, column=0, padx=5, pady=5, ipadx=2, ipady=2)
browse3 = Button(frame, text="Browse", command=lambda: browseLocation(ent3))
browse3.grid(row=3, column=1)

ent4 = Entry(frame, width=80)
ent4.grid(row=4, column=0, padx=5, pady=5, ipadx=2, ipady=2)
browse4 = Button(frame, text="Browse", command=lambda: browseLocation(ent4))
browse4.grid(row=4, column=1)

ent5 = Entry(frame, width=80)
ent5.grid(row=5, column=0, padx=5, pady=5, ipadx=2, ipady=2)
browse5 = Button(frame, text="Browse", command=lambda: browseLocation(ent5))
browse5.grid(row=5, column=1)

#Options Settings
optFrame = Frame(root)
optFrame.pack(side=BOTTOM, fill=Y)

verboseVar = BooleanVar()
silentVar = BooleanVar()
testonlyVar = BooleanVar()
filesVar = BooleanVar()
verboseVar.set(False)
silentVar.set(False)
testonlyVar.set(True)
filesVar.set(False)
verboseCheck = Checkbutton(optFrame, text="Verbose", variable=verboseVar)
silentCheck = Checkbutton(optFrame, text="Silent", variable=silentVar)
testonlyCheck = Checkbutton(optFrame, text="Test Only", variable=testonlyVar)
filesCheck = Checkbutton(optFrame, text="Files Only", variable=filesVar)
verboseCheck.grid(row=0, column=1)
silentCheck.grid(row=0, column=2)
filesCheck.grid(row=0,column=3)
testonlyCheck.grid(row=0, column=4)

var = StringVar()
numericBox = Spinbox(optFrame,width=6,justify=CENTER,from_=1,to=999,textvariable=var)
var.set("7")
numericBox.grid(row=3,column=0,padx=5,pady=5)

dayLabel = Label(optFrame,text="days minimum age before delete", justify=LEFT)
dayLabel.grid(row=3,column=1,columnspan=3)

processButton = Button(optFrame, text='Process', fg="Red", command=startProcess)
processButton.grid(row=3,column=5,padx=5,pady=5,ipadx=2,ipady=2)

browse1.focus()

root.mainloop()
