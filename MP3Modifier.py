from mutagen.id3 import ID3
import os


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


Path = "C:\\Users\\nmaltas\\Documents\\Temp\\Testbench\\BowlingForSoup\\"
FileName = "Cosmic"  # "Bowling For Soup - Alexa Bliss.mp3"
Mpougiournti = Path + FileName

try:
    Kolokythi = ID3(Mpougiournti)
except:
    print(f"No ID3v2 tag found in '{Mpougiournti}'")
    Kolokythi = None

print(Path)
Title = Kolokythi.get("TIT2")
Artist = Kolokythi.get("TPE1")

Title = "Title : " + Title[0].strip()
Artist = "Artist : " + Artist[0].strip()

print(Title)
print(Artist)


print("Hey!!")
