import csv
import fileinput

with open('data.csv', 'rb') as f:
    reader = csv.reader(f)
    csvlist = list(reader)

print csvlist

import fileinput
counter = 0
for values in csvlist:
	print(values)
	if values[0] != '':
		print("New Date, new Week")
		file = fileinput.FileInput('Vorlage.tex', inplace=False)	
    		for line in file:
        		line.replace("$$WOCHE$$", values[0])
		

