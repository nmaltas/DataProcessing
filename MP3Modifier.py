import tkinter as tk
import tkinter.font as tkFont
import glob
import sys
import fileinput
import os
from mutagen.id3 import ID3, ID3NoHeaderError, TIT2, TPE1

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

    def CreateWidgets(self):

        # Setting background color
        BackgroundColor = "#244420"
        self.configure(bg=BackgroundColor)

        # File name entry field and label
        self.FileNameLabel = tk.Label(self, text="File name: ", fg="#FF6600", bg=BackgroundColor)
        self.FileNameLabel.grid(row=0, column=3)
        self.FileNameEntry = tk.Entry(self, width=50)
        self.FileNameEntry.grid(row=1, column=3)

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
        self.DoneButton = tk.Button(self, text="Done. Load next.", bg="#FF6600", activebackground="#FF8040")
        self.DoneButton.grid(row=7, column=3)


# Path = "C:\\Users\\nmaltas\\Documents\\Temp\\Testbench\\BowlingForSoup\\"
# Path = os.path.dirname(__file__)
# FileList = [f for f in os.listdir() if (f.lower().endswith(".mp3") and os.path.isfile(f))]

# print(FileList)

# for File in FileList:

#     try:
#         Artist, Title = File.split(" - ", 1)

#     except Exception as CantSplit:
#         continue

#     try:
#         Kolokythi = ID3(File)

#     except ID3NoHeaderError:
#         print(f"No ID3v2 tag found in '{File}'")
#         Kolokythi = ID3()

#     Kolokythi["TIT2"] = TIT2(encoding=3, text=Title)
#     Kolokythi["TPE1"] = TPE1(encoding=3, text=Artist)
#     Kolokythi.save(os.path.join(Path, File), v2_version=3)

#     os.rename(File, Title)

root = tk.Tk()
Mpifteki = MP3Modifier(root)
root.title("MP3Modifier")
root.geometry("800x300+100+200")

root.mainloop()

print("Hey!!")
