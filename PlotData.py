import matplotlib.pyplot as plt
import numpy as np




x0 = []
y0 = []


################## DATA 1 ############################
Data = open("Data.txt", "r")
Mpougiournti = Data.readlines()
Data.close()
for Line in Mpougiournti[1:]:
    Kolokythia = Line.strip().split(',')
    x0.append(float(Kolokythia[0]))
    y0.append(float(Kolokythia[1]))
    


plt.plot(x0, y0, label="Data", color = "green")
####################################################


plt.xlabel = ("OffsetVal Plot")
plt.ylabel = ("Readings (mV)")
plt.title("A Offset")


plt.grid(True, which = "both", linewidth = 0.5)
# Highlight Area
#plt.axhspan(-50, 50, alpha=0.3, color='orange', label='PASS')
plt.legend()

plt.show()