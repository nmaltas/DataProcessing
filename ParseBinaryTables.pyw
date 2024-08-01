import glob
import os
import binascii

def Decimate(FileI):

    i = 0
    NPath = r'C:/Users/nmaltas/Documents/Temp/Testbench/NTables/'+FileI[(FileI.find("\\")+1):len(FileI)]
    FileI = FileI.replace("\\", "/")

    
    FileO = open(NPath, 'w')

    with open(str(FileI), 'rb') as File:
        while True:
            i = i+1
            Line = File.read(16)
                        

            if not Line:
                break
            
            if ((i-1)%4 == 0):
                
                FileO.write((((binascii.hexlify(Line)).decode('utf-8')) +'\n'))
            
    FileO.close()





Path = r'C:/Users/nmaltas/Documents/Temp/Testbench/Tables'

Files = glob.glob(os.path.join(Path, '*.bin'))

for f in glob.glob(os.path.join(Path, '*.bin')):
    if (not os.path.isfile(f)):
        continue
       
    
    Decimate(f)
    
for f in glob.glob(os.path.join(Path, '*.par')):
    if (not os.path.isfile(f)):
        continue
       
    
    Decimate(f)
    