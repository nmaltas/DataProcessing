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
        self.FileNameEntry = tk.Entry(self, width=50, state="readonly")
        self.FileNameEntry.grid(row=1, column=3)

        # Metadata control fields
        # Title
        self.TitleLabel = tk.Label(self, text="Title: ", fg="#FF6600", bg=BackgroundColor)
        self.TitleLabel.grid(row=2, column=0)
        self.TitleEntry = tk.Entry(self, width=30)
        self.TitleEntry.grid(row=3, column=0)
        # Artist 1
        self.Artist1Label = tk.Label(self, text="Artist 1: ", fg="#FF6600", bg=BackgroundColor)
        self.Artist1Label.grid(row=2, column=3)
        self.Artist1Entry = tk.Entry(self, width=30)
        self.Artist1Entry.grid(row=3, column=3)
        # Artist 2
        self.Artist2Label = tk.Label(self, text="Artist 2: ", fg="#FF6600", bg=BackgroundColor)
        self.Artist2Label.grid(row=2, column=5)
        self.Artist2Entry = tk.Entry(self, width=30)
        self.Artist2Entry.grid(row=3, column=5)

        # File name entry field and label
        self.NewFileNameLabel = tk.Label(self, text="New file name: ", fg="#FF6600", bg=BackgroundColor)
        self.NewFileNameLabel.grid(row=5, column=3)
        self.NewFileNameEntry = tk.Entry(self, width=50)
        self.NewFileNameEntry.grid(row=6, column=3)

        # Execute button
        self.RunButton = tk.Button(self, text="Load", command=self.Main, bg="#FF6600", activebackground="#FF8040")
        self.RunButton.grid(row=7, column=3)

        # Skip button
        self.SkipButton = tk.Button(self, text="Skip", command=self.Skip, bg="#FF6600", activebackground="#FF8040")
        self.SkipButton.grid(row=7, column=2, sticky="e")

        # Swap data button
        self.SwapButton = tk.Button(self, text="\U0001f504", command=self.SwapData, bg="#FF6600", activebackground="#FF8040")
        self.SwapButton.grid(row=3, column=2, sticky="e", padx=50)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)

    ###########################################################################################
    def GetFiles(self):
        FileList = [f for f in os.listdir() if (f.lower().endswith(".mp3") and os.path.isfile(f))]
        print(FileList)
        return FileList

    ###########################################################################################
    def LoadNext(self):
        print(len(self.ItemStorage))
        if len(self.ItemStorage) > 0:
            return self.ItemStorage.popleft()
        else:
            return "Done!"

    ###########################################################################################
    def UnpackFile(self, FileName):

        Splitter = " - "

        self.FileNameEntry.config(state="normal")
        self.FileNameEntry.delete(0, tk.END)
        self.FileNameEntry.config(state="readonly")
        self.TitleEntry.delete(0, tk.END)
        self.Artist1Entry.delete(0, tk.END)
        self.Artist2Entry.delete(0, tk.END)
        self.NewFileNameEntry.delete(0, tk.END)

        with open(FileName, "r") as File:

            if Splitter in FileName:
                self.Artist0, self.Title0 = FileName.split(Splitter, 1)
            else:
                self.Title0 = FileName
                self.Artist0 = FileName

            try:
                self.FileInFocus = ID3(FileName)
                ValidMetadata = True

            except ID3NoHeaderError:
                print(f"No ID3v2 tag found in '{FileName}'")
                self.FileInFocus = ID3()
                ValidMetadata = False

            self.FileNameEntry.config(state="normal")
            self.FileNameEntry.insert(0, FileName)
            self.FileNameEntry.config(state="readonly")

        if ValidMetadata:

            if self.FileInFocus.get("TIT2") != None:
                self.TitleEntry.insert(0, self.FileInFocus.get("TIT2"))
                self.NewFileNameEntry.insert(0, self.FileInFocus.get("TIT2"))
                self.NewFileNameEntry.insert(tk.END, ".mp3")
            if self.FileInFocus.get("TPE1") != None:
                self.Artist1Entry.insert(0, self.FileInFocus.get("TPE1"))
            if self.FileInFocus.get("TPE2") != None:
                self.Artist2Entry.insert(0, self.FileInFocus.get("TPE2"))

        else:
            self.TitleEntry.insert(0, self.Title0[:-4])
            self.Artist1Entry.insert(0, self.Artist0)
            self.Artist2Entry.insert(0, "")
            self.NewFileNameEntry.insert(0, self.Title0)

    ###########################################################################################
    def ModifyFile(self, FileName):
        Title = self.TitleEntry.get()
        if Title == "-":
            del self.FileInFocus["TIT2"]
        elif Title != "":
            self.FileInFocus["TIT2"] = TIT2(encoding=3, text=Title)

        Artist1 = self.Artist1Entry.get()
        if Artist1 == "-":
            del self.FileInFocus["TPE1"]
        elif Artist1 != "":
            self.FileInFocus["TPE1"] = TPE1(encoding=3, text=Artist1)

        Artist2 = self.Artist2Entry.get()
        if Artist2 == "-":
            del self.FileInFocus["TPE2"]
        elif Artist2 != "":
            self.FileInFocus["TPE2"] = TPE2(encoding=3, text=Artist2)

        self.FileInFocus.save(os.path.join(self.Path, FileName), v2_version=3)

        os.rename(FileName, self.NewFileNameEntry.get())

    ###########################################################################################
    def Main(self):

        # Check for empty or done before editing file
        Current = self.FileNameEntry.get()

        if Current == "Done!":
            return
        elif Current == "":
            self.RunButton.config(text="Modify and load next")
        else:
            self.ModifyFile(Current)

        Next = self.LoadNext()

        if Next == "Done!":
            self.FileNameEntry.config(state="normal")
            self.FileNameEntry.delete(0, tk.END)
            self.FileNameEntry.insert(0, Next)
            self.FileNameEntry.config(state="readonly")
            self.TitleEntry.insert(0, "")
            self.Artist1Entry.insert(0, "")
            self.Artist2Entry.insert(0, "")
            self.NewFileNameEntry.insert(0, "")
            return

        else:
            self.UnpackFile(Next)

    ###########################################################################################
    def SwapData(self):
        Temp = self.TitleEntry.get()
        self.TitleEntry.delete(0, tk.END)
        self.TitleEntry.insert(0, self.Artist1Entry.get())
        self.Artist1Entry.delete(0, tk.END)
        self.Artist1Entry.insert(0, Temp)

    ###########################################################################################
    def Skip(self):
        # Check for empty or done before editing file
        Current = self.FileNameEntry.get()

        if Current == "Done!" or Current == "":
            return

        Next = self.LoadNext()

        if Next == "Done!":
            self.FileNameEntry.config(state="normal")
            self.FileNameEntry.delete(0, tk.END)
            self.FileNameEntry.insert(0, Next)
            self.FileNameEntry.config(state="readonly")
            self.TitleEntry.delete(0, tk.END)
            self.Artist1Entry.delete(0, tk.END)
            self.Artist2Entry.delete(0, tk.END)
            self.NewFileNameEntry.delete(0, tk.END)
            return

        else:
            self.UnpackFile(Next)


###########################################################################################
###########################################################################################
###########################################################################################

root = tk.Tk()
Mpifteki = MP3Modifier(root)
root.title("MP3Modifier")
root.geometry("900x400+100+200")

root.mainloop()

print("Hey!!")
