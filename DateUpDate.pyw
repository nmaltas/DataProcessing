from tkinter import *
import tkinter.font as tkFont
import glob
import os
import sys
import fileinput
import datetime


class Interface:
    def __init__(self, win):

        self.default_font = tkFont.nametofont("TkDefaultFont")
        self.default_font.configure(size=16, family="Comic Sans MS")

        # Obtain current date and format it
        self.TodayIs = datetime.datetime.now()
        self.UpDate = str(self.TodayIs.month) + "/" + \
            str(self.TodayIs.day) + "/" + str(self.TodayIs.year)

        # Set the path for the root directory
        self.RootDirPath = 'M:/Testprog/BOEING'
        self.RootPathLabel = Label(text="Root:", fg="#FF6600", bg="#244420")
        self.RootPathLabel.place(x=5, y=10)
        self.RootPathEntry = Entry(width=60, bg="#FF6600")
        self.RootPathEntry.insert(END, self.RootDirPath)
        self.RootPathEntry.place(x=75, y=18)

        # Set the date
        self.DateLabel1 = Label(text="Date:", fg="#FF6600", bg="#244420")
        self.DateLabel1.place(x=5, y=45)
        self.DateLabel2 = Label(text="Format: MM/DD/YYYY",
                                fg="#FF6600", bg="#244420")
        self.DateLabel2.place(x=5, y=75)
        self.DateEntry = Entry(width=15, bg="#FF6600")
        self.DateEntry.place(x=95, y=54)
        self.DateEntry.insert(END, self.UpDate)

        # Run Button
        self.TriggerButton = Button(
            win, text='Run', command=self.Run, bg="#FF6600", activebackground="#FF8040")
        self.TriggerButton.place(x=300, y=55)

    def Run(self):

        # Prepare Parameters
        RootDir = self.RootPathEntry.get()
        RootDir = RootDir.replace("\\", "/")
        NewDate = "CalDate = " + self.DateEntry.get()

        # Obtain a list of all subfolders in directory
        Subfolders = [x[0] for x in os.walk(RootDir)]

        for Path in Subfolders:
            Files = [f.path for f in os.scandir(Path) if (not f.is_dir())]

            # Search each subfolder for .INI files
            for Winner in Files:
                if (Winner[len(Winner) - 3:] == "INI"):

                    # Apply changes if applicable
                    for Line in fileinput.input(Winner, inplace=True):
                        if "CalDate" in Line:
                            print(Line.replace(Line, NewDate))
                        else:
                            print(Line, end="")


App = Tk()
Tzatziki = Interface(App)
App.configure(bg="#244420")
App.title('DateUpDate')
App.geometry("500x130+500+200")
App.mainloop()
