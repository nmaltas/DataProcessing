import datetime as dt
import os
import tkinter as TK
from stat import S_ISDIR

import paramiko


GlobalFont = ('Arial', 15)

HostName = "INSERT IP"
UserName = "INSERT USERNAME"
Password = "INSERT PASSWORD"
DataDirectory = "REMOTE LOCATION"
Destination = "LOCAL LOCATION"

ClientInstance = paramiko.SSHClient()
ClientInstance.set_missing_host_key_policy(paramiko.AutoAddPolicy())


# Reads and creates copies of the data
def GetData(SFTPInstance, DataDirectory, Destination):

    for Stuff in SFTPInstance.listdir_attr(DataDirectory):
        
        if (S_ISDIR(Stuff.st_mode)):
            continue
        
        From = DataDirectory + "/" + Stuff.filename
        To = os.path.join(Destination, Stuff.filename)
        SFTPInstance.get(From, To)


# Attempt to establish a connection to the host
def Run():
    try:
        ClientInstance.connect(HostNameEntry.get(), username = UserNameEntry.get(), password = PasswordEntry.get())

        with ClientInstance.open_sftp() as SFTPInstance:

            GetData(SFTPInstance, EntryFrom.get(), EntryTo.get())

    
        print("Job complete!!")

    except paramiko.AuthenticationException as auth_err:
        print(f"Authentication failed: {auth_err}")

    except paramiko.SSHException as ssh_err:
        print(f"SSH connection failed: {ssh_err}")

    finally:
        # Close the SSH connection
        ClientInstance.close()


######################################## Basic GUI Setup ###############################

# Window Setup
Root = TK.Tk()
Root.title("GetData")
Root.geometry("500x300")
Root.option_add("*Font", GlobalFont)
Root.configure(bg="#005288")

# SSH credentials
CredentialsLabel = TK.Label(text= "Credentials", bg ="#005288", fg="#E6E6E6")
CredentialsLabel.place(x=125, y=0)

# HostName
HostNameLabel = TK.Label( text = "Hostname: ", bg ="#005288", fg="#E6E6E6")
HostNameLabel.place(x=15, y=40)

HostNameEntry = TK.Entry(width=13, bg="#E6E6E6")
HostNameEntry.place(x=125, y=40)
HostNameEntry.insert(0, HostName)

# UserName
UserNameLabel = TK.Label( text = "Username: ", bg ="#005288", fg="#E6E6E6")
UserNameLabel.place(x=15, y=80)

UserNameEntry = TK.Entry(width=13, bg="#E6E6E6")
UserNameEntry.place(x=125, y=80)
UserNameEntry.insert(0, UserName)

# Password
PasswordLabel = TK.Label( text = "Password: ", bg ="#005288", fg="#E6E6E6")
PasswordLabel.place(x=15, y=120)

PasswordEntry = TK.Entry(width=13, show="+", bg="#E6E6E6")
PasswordEntry.place(x=125, y=120)
PasswordEntry.insert(0, Password)

# Entry Field From
LabelFrom = TK.Label( text = "From: ", bg ="#005288", fg="#E6E6E6")
LabelFrom.place(x=15, y=200)

EntryFrom = TK.Entry(width=40, font=13, bg="#E6E6E6")
EntryFrom.place(x=90, y=205)
EntryFrom.insert(0, DataDirectory)

# Entry Field To
LabelTo = TK.Label(text = "To: ", bg ="#005288", fg="#E6E6E6")
LabelTo.place(x=15, y=250)

EntryTo = TK.Entry(width=40, font=13, bg="#E6E6E6")
EntryTo.place(x=90, y=252)
EntryTo.insert(0, Destination)

# Run Button
Trigger = TK.Button(Root, text="Run", command = Run, bg="#E6E6E6", activebackground="#FF8040", fg="#005288", activeforeground="#005288", width =9, height=2, font= ('Arial',22))
Trigger.place(x=300, y=50)

###################################################################################

Root.mainloop()