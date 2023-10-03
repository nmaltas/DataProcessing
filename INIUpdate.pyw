from tkinter import *
import tkinter.font as tkFont
import glob
import os
import sys
import fileinput
import datetime


class Interface:
    def __init__(self, win)

        self.default_font = tkFont.nametofont("TkDefaultFont")
        self.default_font.configure(size=16, family="Comic Sans MS")

        # Set the path for the root directory
        #self.RootDirPath = r"'M:\Testprog\BOEING"
        self.RootDirPath = r"Insert Path"
        self.RootPathLabel = Label(text="Root:", fg="#FF6600", bg="#244420")
        self.RootPathLabel.place(x=5, y=10)
        self.RootPathEntry = Entry(width=60, bg="#FF6600")
        self.RootPathEntry.insert(END, self.RootDirPath)
        self.RootPathEntry.place(x=75, y=18)

        # Parameter selection
        self.ParameterLabel = Label(
            text="Select Parameter", fg="#FF6600", bg="#244420")

        self.ParameterLabel.place(x=5, y=45)

        # Dropdown menu with available parameters
        ###############################################################################################
        # List of parameters to change in the files. Add new parameters at the end if needed.
        # IT IS IMPORTANT THAT PARAMETERS ARE TYPED CORRECTLY WHEN ADDED!!tele
        # Do not forget to add notes to the ParameterNotes below after adding a new parameter to the list. Make a placeholder if there are no notes.
        self.Parameters = ["TxOutPwrCbl", "CalDate", "RxSensLower", "RxSensUpper",
                           "StartValHigh", "StartValLow", "StartValComp", "RxPwrSenComp", "TxA", "TxB", "FWD_RxA", "AFT_RxA", "AFT_RxB", "FWD_TxA_Upper", "FWD_TxA_Lower", "AFT_TxA_Upper", "AFT_TxA_Lower", "AFT_TxB_Upper", "AFT_TxB_Lower", "Guardband", "ThreshCalFactor", "AftPercentChange", "FwdPercentChange", "AftStartValueA", "AftStartValueB", "FwdStartValue"
                           ]
        ###############################################################################################

        self.DropdownVariable = StringVar(App)
        # self.DropdownVariable.set(self.Parameters[1])  # Default value
        self.ParametersDropdown = OptionMenu(
            App, self.DropdownVariable, *self.Parameters, command=self.ChangeNotes)
        self.ParametersDropdown.config(
            bg="#FF6600", activebackground="#FF6600", highlightthickness=0, fg="#244420")
        self.ParametersDropdown["menu"].config(
            bg="#FF6600", activebackground="#228B22", activeforeground="black", borderwidth=0)
        self.ParametersDropdown.pack()
        self.ParametersDropdown.place(x=5, y=80)

        # New value
        self.NewValueLabel = Label(
            text="New Value", fg="#FF6600", bg="#244420")
        self.NewValueLabel.place(x=5, y=125)

        self.NewValue = Entry(width=25, bg="#FF6600")
        self.NewValue.place(x=10, y=165)

        # Run Button
        self.TriggerButton = Button(
            win, text='Run', command=self.Run, bg="#FF6600", activebackground="#FF8040")
        self.TriggerButton.place(x=10, y=200)

        # Notes Label
        self.Notes = Label(text="Attention!! \nEvery .INI file under the root directory will be affected.\nMake sure that you have selected the right directory and parameter!",
                           wraplength=300, fg="red", bg="#244420", font=("Arial", 12))
        self.Notes.place(x=233, y=65)
        self.a = 5

    def Run(self):

        # Prepare Parameters
        RootDir = self.RootPathEntry.get()
        RootDir = RootDir.replace("\\", "/")
        VariableToBeChanged = self.DropdownVariable.get()
        NewLine = VariableToBeChanged + " = " + self.NewValue.get()
        print(NewLine)

        # Obtain a list of all subfolders in directory
        Subfolders = [x[0] for x in os.walk(RootDir)]

        for Path in Subfolders:
            Files = [f.path for f in os.scandir(Path) if (not f.is_dir())]

            # Search each subfolder for .INI files
            for Winner in Files:
                if (Winner[len(Winner) - 3:] == "INI"):

                    # Apply changes
                    self.ReplaceSequence(Winner, VariableToBeChanged, NewLine)

    def ReplaceSequence(self, Winner, VariableToBeChanged, NewLine):    # Function for changing a specific character sequence in the file
        for Line in fileinput.input(Winner, inplace=True):
            if VariableToBeChanged in Line:
                print(Line.replace(Line, NewLine)).0
                #sys.stderr.write(Winner + "\n")
                #sys.stderr.write(Line + "\n")
            else:
                print(Line, end="") #Do nothing. Prints the same line with no additional \n

    def ChangeNotes(self, event):
        # Notes to be displayed whenever a parameter is chosen
        #########################################################################################################
        # Add notes for parameters here. Order of parameters does not matter.
        ParameterNotes = {
            "TxOutPwrCbl": "Add notes for parameter TxOutPwrCbl",
            "CalDate": "This needs to be at most 1 year before current date.\nFormat must be MM/DD/YYYY",
            "RxSensLower": "Add notes for parameter " + self.DropdownVariable.get(),
            "RxSensUpper": "Add notes for parameter " + self.DropdownVariable.get(),
            "StartValHigh": "Add notes for parameter " + self.DropdownVariable.get(),
            "StartValLow": "Add notes for parameter " + self.DropdownVariable.get(),
            "StartValComp": "Add notes for parameter " + self.DropdownVariable.get(),
            "RxPwrSenComp": "Add notes for parameter " + self.DropdownVariable.get(),
            "TxA": "Add notes for parameter " + self.DropdownVariable.get(),
            "TxB": "Add notes for parameter " + self.DropdownVariable.get(),
            "FWD_RxA": "Add notes for parameter " + self.DropdownVariable.get(),
            "AFT_RxA": "Add notes for parameter " + self.DropdownVariable.get(),
            "AFT_RxB": "Add notes for parameter " + self.DropdownVariable.get(),
            "FWD_TxA_Upper": "Add notes for parameter " + self.DropdownVariable.get(),
            "FWD_TxA_Lower": "Add notes for parameter " + self.DropdownVariable.get(),
            "AFT_TxA_Upper": "Add notes for parameter " + self.DropdownVariable.get(),
            "AFT_TxA_Lower": "Add notes for parameter " + self.DropdownVariable.get(),
            "AFT_TxB_Upper": "Add notes for parameter " + self.DropdownVariable.get(),
            "AFT_TxB_Lower": "Add notes for parameter " + self.DropdownVariable.get(),
            "Guardband": "Add notes for parameter " + self.DropdownVariable.get(),
            "ThreshCalFactor": "Add notes for parameter " + self.DropdownVariable.get(),
            "AftPercentChange": "Add notes for parameter " + self.DropdownVariable.get(),
            "FwdPercentChange": "Add notes for parameter " + self.DropdownVariable.get(),
            "AftStartValueA": "Add notes for parameter " + self.DropdownVariable.get(),
            "AftStartValueB": "Add notes for parameter " + self.DropdownVariable.get(),
            "FwdStartValue": "Add notes for parameter " + self.DropdownVariable.get()
        }
        #########################################################################################################
        self.Notes.config(text=ParameterNotes[self.DropdownVariable.get()])


App = Tk()
Tzatziki = Interface(App)
App.configure(bg="#244420")
App.title('DateUpDate')
App.geometry("570x330+500+200")
App.mainloop()
