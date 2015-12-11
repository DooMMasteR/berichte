import csv
import shutil
import fileinput
import subprocess
import shlex

csvfilename = 'data.csv'
name = 'Gerrit Kaul'
abteilung = 'IS-E'
ausbildungsjahr = 2

with open(csvfilename, 'rb') as f:
    reader = csv.reader(f)
    csvlist = list(reader)

print csvlist

def descriptionlinebuild(lvalues):
    print('Building Desc')
    description = ''
    if(len(lvalues[len(lvalues) -1]) > 3):
        hoursum = lvalues[len(lvalues) -1][3]
    else:
        hoursum = ''
    while(len(lvalues) < 5):
        lvalues.append(['','','',''])
    lvalues_list_len = len(lvalues)
    for counter in range(0, lvalues_list_len):
        if counter + 1  == lvalues_list_len:
            if(lvalues[counter][1] == '' or lvalues[counter][2] == ''):
                description = description + '&' + lvalues[counter][1] +' &' + lvalues[counter][2] + '\n\\\\\\tabucline[2pt]{1}\n\\tabulinestyle{2pt}\n\\multicolumn2{|r}{Summe: } \\vline & ' + hoursum + ' h \\\\\\tabucline[2pt]{1}'
            else:
                description = description + '&' + lvalues[counter][1] +' &' + lvalues[counter][2] + ' h\n\\\\\\tabucline[2pt]{1}\n\\tabulinestyle{2pt}\n\\multicolumn2{|r}{Summe: } \\vline & ' + hoursum + ' h \\\\\\tabucline[2pt]{1}'
        else:
            if(lvalues[counter][1] == '' or lvalues[counter][2] == ''):
                description = description + '&' + lvalues[counter][1] +' &' + lvalues[counter][2] + '\\\\\cline{2-3}\n'
            else:
                description = description + ' &' + lvalues[counter][1] +' &' + lvalues[counter][2] + ' h\\\\\cline{2-3}\n'
    return description
newfilename = ''
counter = 0
valueslist = None
newfile = None
for values in csvlist:
    # print(values)
    if values[0] != '' and values[0] != 'Datum':
        date = values[0]
        if(valueslist is not None and valueslist != []):
            descriptiontex = descriptionlinebuild(valueslist)
            readfile = open(newfilename, 'rt')
            for line in readfile:
                newfile.write(line.replace('%%DESC%%', descriptiontex))
            newfile.close()
        print("New Date, new Week")
        if(counter >0):
            proc=subprocess.Popen(shlex.split('pdflatex ' + newfilename))
            proc.communicate()
        counter += 1
        newfilename = str(counter).zfill(3) + '.tex'
        newfile = open(newfilename, mode='w')
        valueslist = []
        with open("Vorlage.tex", "rt") as fin:
            for line in fin:
                newfile.write(line.replace('%%WOCHE%%', date).replace('%%NAME%%', name).replace('%%DIVIS%%', abteilung).replace('%%YEAR%%', str(ausbildungsjahr)))
        newfile.seek(0)
    elif (values[0] == '' and values[1] != ''):
        values[1] = str(values[1]).replace('&', '\&')
        print(values)
        tvalues = []
        valueslist.append(values)
if(valueslist is not None and valueslist != []):
    descriptiontex = descriptionlinebuild(valueslist)
    readfile = open(newfilename, 'rt')
    for line in readfile:
        newfile.write(line.replace('%%DESC%%', descriptiontex))
    newfile.close()
    proc=subprocess.Popen(shlex.split('pdflatex ' + newfilename))
    proc.communicate()


