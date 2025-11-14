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


# Path = "C:\\Users\\nmaltas\\Documents\\Temp\\Testbench\\BowlingForSoup\\"
Path = os.path.dirname(__file__)
FileList = [f for f in os.listdir() if (f.lower().endswith(".mp3") and os.path.isfile(f))]

print(FileList)

for File in FileList:

    try:
        Artist, Title = File.split(" - ", 1)

    except Exception as CantSplit:
        continue

    try:
        Kolokythi = ID3(File)

    except ID3NoHeaderError:
        print(f"No ID3v2 tag found in '{File}'")
        Kolokythi = ID3()

    Kolokythi["TIT2"] = TIT2(encoding=3, text=Title)
    Kolokythi["TPE1"] = TPE1(encoding=3, text=Artist)
    Kolokythi.save(os.path.join(Path, File), v2_version=3)

    os.rename(File, Title)

print("Hey!!")
