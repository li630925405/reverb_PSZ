import pandas as pd 
import matplotlib.pyplot as plt

acc = pd.read_csv("0616/results_ACC_reverb_0.csv")
acc_3 = pd.read_csv("0616/results_ACC_reverb_3.csv")
acc_10 = pd.read_csv("0616/results_ACC_reverb_10.csv")
pm = pd.read_csv("0616/results_PM_reverb_0.csv")
pm_3 = pd.read_csv("0616/results_PM_reverb_3.csv")
pm_10 = pd.read_csv("0616/results_PM_reverb_10.csv")

# print(acc['Frequency'].shape)
# print(acc['Contrast'])
# input()


fig = plt.figure(figsize=(6, 6), dpi=1000)
axes = fig.add_subplot(111)
axes.semilogx(acc['Frequency'], acc['Contrast'], label="ACC")
axes.semilogx(pm['Frequency'], pm['Contrast'], label="PM")
axes.grid(which='major', linestyle='-', linewidth='0.5', color='black')
axes.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
axes.set_xlabel('Frequency (Hz)')
axes.set_ylabel('Decibels')
axes.set_title("ACC & PM contrast")
axes.legend()

fig.savefig("0616/ACC & PM contrast.jpg")


fig = plt.figure(figsize=(6, 6), dpi=1000)
axes = fig.add_subplot(111)
axes.semilogx(acc['Frequency'], acc['Effort'], label="ACC")
axes.semilogx(pm['Frequency'], pm['Effort'], label="PM")
axes.grid(which='major', linestyle='-', linewidth='0.5', color='black')
axes.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
axes.set_xlabel('Frequency (Hz)')
axes.set_ylabel('Decibels')
axes.set_title("ACC & PM effort")
axes.legend()

fig.savefig("0616/ACC & PM effort.jpg")


fig = plt.figure(figsize=(6, 6), dpi=1000)
axes = fig.add_subplot(111)
axes.semilogx(acc['Frequency'], acc['Contrast'], label="0")
axes.semilogx(acc_3['Frequency'], acc_3['Contrast'], label="3")
axes.semilogx(acc_10['Frequency'], acc_10['Contrast'], label="10")
axes.grid(which='major', linestyle='-', linewidth='0.5', color='black')
axes.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
axes.set_xlabel('Frequency (Hz)')
axes.set_ylabel('Decibels')
axes.set_title("ACC reverb contrast")
axes.legend()

fig.savefig("0616/ACC reverb contrast.jpg")


fig = plt.figure(figsize=(6, 6), dpi=1000)
axes = fig.add_subplot(111)
axes.semilogx(pm['Frequency'], pm['Contrast'], label="0")
axes.semilogx(pm_3['Frequency'], pm_3['Contrast'], label="3")
axes.semilogx(pm_10['Frequency'], pm_10['Contrast'], label="10")
axes.grid(which='major', linestyle='-', linewidth='0.5', color='black')
axes.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
axes.set_xlabel('Frequency (Hz)')
axes.set_ylabel('Decibels')
axes.set_title("PM reverb contrast")
axes.legend()

fig.savefig("0616/PM reverb contrast.jpg")
# plt.show()
