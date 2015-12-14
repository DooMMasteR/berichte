# -*- coding: utf-8 -*-
import csv
import shutil
import fileinput
import subprocess
import shlex

csvfilename = 'data.csv'
name = 'Gerrit Kaul'
abteilung = 'IS-E'
ausbildungsjahr = 2
subjects = ['Deutsch', 'ITS-A', 'ITS-T', 'Englisch', 'AWSYS', 'Politik', 'BWPRO']

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
        lvalues.append(['', '', '', ''])
    lvalues_list_len = len(lvalues)
    for counter in range(0, lvalues_list_len):
        if counter + 1  == lvalues_list_len:
            if(lvalues[counter][1] == '' or lvalues[counter][2] == ''):
                description = description + '&' + lvalues[counter][1] +' &' + lvalues[counter][2] + '\n\\\\\\tabucline[2pt]{1}\n\\tabulinestyle{2pt}\n\\multicolumn2{|r}{Summe: } \\vline & ' + hoursum + ' h \\\\\\tabucline[2pt]{1}'
            else:
                description = description + '&' + lvalues[counter][1] +' &' + lvalues[counter][2] + ' h\n\\\\\\tabucline[2pt]{1}\n\\tabulinestyle{2pt}\n\\multicolumn2{|r}{Summe: } \\vline & ' + hoursum + ' h \\\\\\tabucline[2pt]{1}'
        else:
            if(lvalues[counter][1] == '' or lvalues[counter][2] == ''):
                description = description + '&' + lvalues[counter][1] +' &' + lvalues[counter][2] + '\\\\\\cline{2-3}\n'
            else:
                description = description + ' &' + lvalues[counter][1] +' &' + lvalues[counter][2] + ' h\\\\\\cline{2-3}\n'
    return description

def schooltexbuild(lsvalues):
    if (len(lsvalues) == 0):
        return ''
    builtschooltex = '\\begin{tabu} to \\linewidth {|[2pt]X[c,0.02]|X[l,0.26]|X[l,1.9]|[2pt]}\n\\tabucline[2pt]{1}\n\\multirow{-3}{*}{\\rotatebox{90}{\\textbf{\\parbox[centering]{4cm}{Unterrichts- \\newline themen}}}}\n'
    for clsvalue in lsvalues:
        builtschooltex = builtschooltex + '& ' + clsvalue[0] + ' & ' + clsvalue[1] + ' \\\\\\cline{2-3}\n'
    for i in range(0, 5 - len(lsvalues)):
        builtschooltex = builtschooltex + '& & \\\\\\cline{2-3}\n'
    builtschooltex = builtschooltex + '\\tabucline[2pt]{1}\\end{tabu}\n\\vspace{9mm}\\\\'
    return builtschooltex

newfilename = ''
counter = 0
valueslist = None
svalues = None
newfile = None


for values in csvlist:
    # print(values)
    if values[0] != '' and values[0] != 'Datum' and values[0] not in subjects:
        date = values[0]
        descriptiontex = ''
        if(valueslist is not None and valueslist != []):
            descriptiontex = descriptionlinebuild(valueslist)
        print("New Date, new Week")
        schooltex = ''
        if(svalues is not None and svalues != []):
            schooltex = schooltexbuild(svalues)
        if(schooltex or descriptiontex):
            readfile = open(newfilename, 'rt')
            for line in readfile:
                newfile.write(line.replace('%%DESC%%', descriptiontex).replace('%%SCHOOL%%', schooltex))
            newfile.seek(0)
        if(newfile):
            newfile.close()
        if(counter >0):
            proc=subprocess.Popen(shlex.split('pdflatex ' + newfilename))
            proc.communicate()
        counter += 1
        newfilename = str(counter).zfill(3) + '.tex'
        newfile = open(newfilename, mode='w')
        valueslist = []
        svalues=[]
        with open("Vorlage.tex", "rt") as fin:
            for line in fin:
                newfile.write(line.replace('%%WOCHE%%', date).replace('%%NAME%%', name).replace('%%DIVIS%%', abteilung).replace('%%YEAR%%', str(ausbildungsjahr)).replace('%%NUMBER%%', str(counter).zfill(3)))
        newfile.seek(0)
    elif (values[0] == '' and values[1] != ''):
        values[1] = str(values[1]).replace('&', '\&')
        print(values)
        valueslist.append(values)
    elif (values[0] in subjects and values[1] and values[1] != ''):
        print(values)
        svalues.append([values[0], values[1]])

if(valueslist is not None and valueslist != []):
    descriptiontex = descriptionlinebuild(valueslist)
    readfile = open(newfilename, 'rt')
    for line in readfile:
        newfile.write(line.replace('%%DESC%%', descriptiontex))
    newfile.close()
    proc=subprocess.Popen(shlex.split('pdflatex ' + newfilename))
    proc.communicate()

proc=subprocess.Popen(shlex.split('find . -name "*.log" -delete'))
proc.communicate()
proc=subprocess.Popen(shlex.split('find . -name "*.aux" -delete'))
proc.communicate()



