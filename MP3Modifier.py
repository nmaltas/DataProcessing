import tkinter as tk
import tkinter.font as tkFont
import glob
import sys
import fileinput
import os
from mutagen.id3 import ID3, ID3NoHeaderError, TIT2, TPE1, TPE2
from collections import deque

# Cheatsheet :
# TIT2   = Title
# TPE1   = Lead performer / artist
# TALB   = Album
# TCON   = Content type / genre
# TRCK   = Track number
# TYER   = Year
# TPE2   = Band/orchestra/accompaniment
# COMM   = Comment
# TCOP   = Copyright message
# TPOS   = Part of a set (disc number)
# APIC   = Attached picture (album art)


###########################################################################################
###########################################################################################
class MP3Modifier(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.default_font = tkFont.nametofont("TkDefaultFont")
        self.default_font.configure(size=16, family="Comic Sans MS")

        for i in range(10):
            self.rowconfigure(i, weight=1)
            self.columnconfigure(i, weight=1)

        self.CreateWidgets()
        self.pack(fill="both", expand=True)

        self.Path = os.path.dirname(__file__)
        self.ItemStorage = deque()
        self.ItemStorage.extend(self.GetFiles())
        self.FileInFocus = None
        self.Title0 = None
        self.Artist0 = None

    ###########################################################################################
    def CreateWidgets(self):

        # Setting background color
        BackgroundColor = "#244420"
        self.configure(bg=BackgroundColor)

        # File name entry field and label
        self.FileNameLabel1 = tk.Label(self, text="File name: ", fg="#FF6600", bg=BackgroundColor)
        self.FileNameLabel1.grid(row=0, column=3)
        self.FileNameLabel2 = tk.Label(self, text="", fg="#FF6600", bg=BackgroundColor)
        self.FileNameLabel2.grid(row=1, column=3)

        # Metadata control fields
        # Title
        self.TitleLabel = tk.Label(self, text="Title: ", fg="#FF6600", bg=BackgroundColor)
        self.TitleLabel.grid(row=2, column=0)
        self.TitleEntry = tk.Entry(self, width=25)
        self.TitleEntry.grid(row=3, column=0)
        # Artist 1
        self.Artist1Label = tk.Label(self, text="Artist 1: ", fg="#FF6600", bg=BackgroundColor)
        self.Artist1Label.grid(row=2, column=3)
        self.Artist1Entry = tk.Entry(self, width=25)
        self.Artist1Entry.grid(row=3, column=3)
        # Artist 2
        self.Artist2Label = tk.Label(self, text="Artist 2: ", fg="#FF6600", bg=BackgroundColor)
        self.Artist2Label.grid(row=2, column=5)
        self.Artist2Entry = tk.Entry(self, width=25)
        self.Artist2Entry.grid(row=3, column=5)

        # File name entry field and label
        self.NewFileNameLabel = tk.Label(self, text="New file name: ", fg="#FF6600", bg=BackgroundColor)
        self.NewFileNameLabel.grid(row=5, column=3)
        self.NewFileNameEntry = tk.Entry(self, width=50)
        self.NewFileNameEntry.grid(row=6, column=3)

        # Execute button
        self.RunButton = tk.Button(self, text="Load", command=self.Run, bg="#FF6600", activebackground="#FF8040")
        self.RunButton.grid(row=7, column=3)

    ###########################################################################################
    def GetFiles(self):
        FileList = [f for f in os.listdir() if (f.lower().endswith(".mp3") and os.path.isfile(f))]
        print(FileList)
        return FileList

    ###########################################################################################
    def LoadNext(self):
        if len(self.ItemStorage) > 0:
            return self.ItemStorage.popleft()
        else:
            return "Done!"

    ###########################################################################################
    def UnpackFile(self, FileName):
        with open(FileName, "r") as File:
            try:
                self.Artist0, self.Title0 = FileName.split(" - ", 1)

            except Exception as CantSplit:
                self.Title0 = FileName

            try:
                self.FileInFocus = ID3(FileName)
                ValidMetadata = True

            except ID3NoHeaderError:
                print(f"No ID3v2 tag found in '{FileName}'")
                self.FileInFocus = ID3()
                ValidMetadata = False

            self.FileNameLabel2.config(text=FileName)

        if ValidMetadata:

            # bug here. IF a tag gets loaded in a (local, no need to make it accessible to the entire class) variable, then do:
            self.TitleEntry.insert(0, self.FileInFocus.get("TIT2"))
            self.Artist1Entry.insert(0, self.FileInFocus.get("TPE1"))
            self.Artist2Entry.insert(0, self.FileInFocus.get("TPE2"))

            self.NewFileNameEntry.insert(0, self.FileInFocus.get("TIT2") + ".mp3")

        else:
            self.TitleEntry.insert(0, self.Title0[:-4])
            self.Artist1Entry.insert(0, self.Artist0)
            self.Artist2Entry.insert(0, "")

            self.NewFileNameEntry.insert(0, self.Title0)

    ###########################################################################################
    def ModifyFile(self, FileName):
        Title = self.TitleEntry.get()
        self.FileInFocus["TIT2"] = TIT2(encoding=3, text=Title)
        self.FileInFocus["TPE1"] = TPE1(encoding=3, text=self.Artist1Entry.get())

        Artist2 = self.Artist2Entry.get()

        if Artist2 != "":
            self.FileInFocus["TPE2"] = TPE2(encoding=3, text=Artist2)

        self.FileInFocus.save(os.path.join(self.Path, FileName), v2_version=3)

        os.rename(FileName, Title)

    ###########################################################################################
    def Run(self):

        # Check for empty or done before editing file
        Current = self.FileNameLabel2.cget("text")

        if Current == "Done":
            return
        elif Current == "":
            self.RunButton.config(text="Done. Load next.")
        else:
            self.ModifyFile(Current)

        Next = self.LoadNext()

        if Next == "Done":
            self.FileNameLabel2.config(text=Next)
            self.TitleEntry.insert(0, "")
            self.Artist1Entry.insert(0, "")
            self.Artist2Entry.insert(0, "")
            self.NewFileNameEntry.insert(0, "")
            return

        else:
            self.UnpackFile(Next)


###########################################################################################
###########################################################################################
###########################################################################################

root = tk.Tk()
Mpifteki = MP3Modifier(root)
root.title("MP3Modifier")
root.geometry("800x300+100+200")

root.mainloop()

print("Hey!!")
