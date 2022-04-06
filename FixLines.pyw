from tkinter import *
import tkinter.font as tkFont
import glob
import os
    
class Interface:
    def __init__(self, win):
        #Set Font parameters
        self.default_font = tkFont.nametofont("TkDefaultFont")
        self.default_font.configure(size=16, family = "Comic Sans MS")
         
        #Default LineSize
        self.LineSize = 300   #Optimal = 300
        
        #Variable for the checkbox
        self.CheckMe = IntVar()
        
        #Run Script Button
        self.Run = Button( win, text = 'Run Script', command = self.ModeSelector, bg = "#FF8040",  activebackground = "#FF8040")
        self.Run.place( x = 400 - 70, y = 400 )
        
        #Labels and Entry Fields
        
        #Input File
        self.InputLabel = Label( text = "Select your file to be modified", fg = "white", bg = "#1C286C")
        self.InputLabel.place(x = 70 , y = 60)
        self.InputFile = Entry(width = 25)
        self.InputFile.place(x = 130 , y = 100, height = 21)
        
        #Output File
        self.OutputLabel = Label( text = "Select your output file", fg = "white", bg = "#1C286C")
        self.OutputLabel.place(x = 490, y = 60)
        self.OutputFile = Entry(width = 25)
        self.OutputFile.place(x = 520, y = 100, height = 21)
        
        #Line Size
        self.LineSizeLabel = Label(text = "Set desired line length :", fg = "white", bg = "#1C286C")
        self.LineSizeLabel.place(x = 130, y  = 240)
        self.LineSizeInput = Entry(width = 5)
        self.LineSizeInput.place( x = 380, y = 250, height = 21)
        self.LineSizeInput.insert(END, str(self.LineSize))
        
        #Checkboz for GlobalMode
        self.CheckAll = Checkbutton(variable=self.CheckMe, onvalue=1, offvalue=0, command=self.ToggleCheckbox, fg = "black", bg = "#1C286C",  activebackground = "#1C286C", activeforeground="white", selectcolor = "#FF8040")
        self.CheckAll.place(x = 290, y  = 140)
        self.CheckAllLabel = Label(text='Do for all files in directory', fg = "white", bg = "#1C286C")
        self.CheckAllLabel.place(x = 10, y  = 140)
        
    #The checkbox controls whether the Input File entyr field is available
    def ToggleCheckbox(self):
        if (self.CheckMe.get() == 1):
            self.InputFile.config(state= "disabled")
        else :
            self.InputFile.config(state= "normal")
    
    #Depending on the checkbox value the mode gets selected
    def ModeSelector(self):
        if (self.CheckMe.get() == 1):
            self.GlobalMode()
        else:
            self.SingleMode()
    
    #Single Input mode
    def SingleMode(self):
        FileI = self.GetInputFile( self.InputFile.get())        #Generate input file name
        if (FileI == ".txt"):                                   #Check if input file entry field was empty
            return
        FileO = self.GetOutputFile(FileI, self.OutputFile.get())            #Generate output file name
        self.Rectify(FileI, FileO)          #Run the script for one input
    
    #Global input mode
    def GlobalMode(self):
        Files = glob.glob('*.txt')                                      #Obtain all .txt files from directory
        TempOutFile = self.OutputFile.get()
        print(TempOutFile)
        Iterator = 1
        for kolokythi in Files:
            FileO = self.GetOutputFile(str(kolokythi),  TempOutFile)
            if (TempOutFile != ""):           # Modify output file properly so that the iterator doesnt mess up with the .txt suffix.
                FileO = FileO[0:len(FileO)-4] +str(Iterator) + FileO[len(FileO)-4:len(FileO)]
            self.Rectify(kolokythi, self.GetOutputFile(kolokythi, FileO)) #Run main script for each file. 
            Iterator = Iterator + 1
    
    #Input file parameters  
    def GetInputFile(self, FileName):
        if ( FileName[len(FileName) - 4 : len(FileName)] != ".txt" ):
            FileName = FileName + ".txt"
        
        return FileName
    
    #Output file parameters  
    def GetOutputFile(self, FileI, FileName):
        
        if ((FileName == "") ):
            FileName = "N" + FileI
        
        elif ( FileName[len(FileName) - 4 : len(FileName)] != ".txt") :
            FileName = FileName + ".txt"
         
        return FileName
    
    # The main script is here
    def Rectify(self, FileI, FileO):
        #Obtain LineSize parameter
        self.LineSize = int(self.LineSizeInput.get())
        if (self.LineSize < 3):          #Don't deal with unreasonable parameters
            return

        #Check and handle file I/O parameters
        
        #Set the file handles
        RawText = open(FileI, encoding = "UTF-8", mode = 'r')           #UTF-8 encoding so that other languages than english can be read
        Output = open(FileO, encoding = "UTF-8", mode = 'w')

        #Algorithm starts here
        Counter  = 0
        Line3 = ""
        for Line1 in RawText:       #For each line
            if (Line1[0] == '\n') :
                continue
            else :
                Line2 = Line1.lstrip()          #Remove redundant \w  on left side of line
            
                for Character in Line2:
                
                    if ((Character == '\n') & (Counter == 0)):      #Remove empty lines
                        continue
                    
                    elif (Character == '\n'):       #End of a line
                        Output.write(Line3 + "\n")
                        Counter  = 0
                        Line3 = ""
                    else :          #Normaly run and add characters to the new line
                        if ( (str.isspace(Character)) & (Counter == 0) ):               #Remove \w if line was broken at full word
                            continue
                        Line3 = Line3 + Character
                        Counter = Counter + 1
                
                    if (Counter == self.LineSize):                  #Line is at maximum, it needs to end
                        if ( ~str.isspace(Line2[Counter + 1])):         #If not at the end of a word
                            Line3 = self.WordBreak(Line3, Output, self.LineSize)            #Special function for not breaking words
                            try: 
                                Counter = len(Line3)                        #Keep the broken word and continue to the next line with it
                            except:
                                Counter = 0                                         #This happens when the broken word is bigger than the maximum line size
                            continue
                        
                        #Export the line and reset
                        Output.write(Line3 + "\n")
                        Line3 = ""
                        Counter = 0
        
        #After out of the loop, dump the text and close all files
        Output.write(Line3)
        Output.close()
        RawText.close()
        return
    
    #Special function for not breaking words
    def WordBreak( self, Line, Output, LineSize):
        CheckPoint = ""
        Iterator = LineSize
        
        #Seek for the beginning of the broken word
        while ( Iterator >= 0 ):
            if (Iterator == 0): #If word is as long as maximum line length
                Output.write(Line + "\n")   #Dump it broken as it is and go back
                return  CheckPoint
            if ( str.isspace(Line[Iterator-1])):    #Otherwise when the beginning is found move on
                break
            
            Iterator = Iterator -1
            
        #Dump the line without the broken word
        Output.write(Line[0:Iterator-1] + "\n")
        
        #Save the broken word for the next line
        CheckPoint = Line[Iterator:LineSize]
        
        #Return the broken word for the next line
        return CheckPoint

App=Tk()
Mpougiounti= Interface(App)
App.configure( bg = "#1C286C")
App.title('TextLinesFix')
App.geometry("800x500+500+200")
App.mainloop()
