""" Prepare National Longitudinal Survey data, 1997-2013.

    - Hypothesis: Any conditions from childhood are essentially absorbing states,
        or, non-ergodic. The probability that a child in a certain strata of
        weight leaves that strata is near zero, and transitions to any other
        state other than the one immediately adjacent to it is in fact zero (as 
        in, no one jumps from underweight to obese in one year)

    .NLSY97 contains all variable IDs, and demographicBMIVars are a subset of 
    those variables on demographic and height/weight, pulled from the Investigator
    website (https://www.nlsinfo.org/investigator/pages/search.jsp). This script
    collects those variables, and trims a subset of the full NLSY97 dataset to a
    manageable size for further analysis. 

    Inputs: demographicBMIVars.NLYS97, nlsy97_all_1997-2013.NLSY97, nlsy97_all_1997-2013.dat
    Outputs: nlsy97_demographicBMI.json

    Author: Seth Rhoades
"""
import csv, json
import pandas as pd 
csv.field_size_limit(1000000)

subKeys = []
with open('demographicBMIVars.NLSY97') as fin:
    csvReader = csv.reader(fin)
    for row in csvReader:
        subKeys.append(row[0])

allKeys = []
with open('nlsy97_all_1997-2013.NLSY97') as fin:
    csvReader = csv.reader(fin)
    for row in csvReader:
        allKeys.append(row[0])

subLocs = []
for i, j in enumerate(allKeys):
    for subKey in subKeys:
        if j == subKey:
            subLocs.append(i) #Var loc on dataEntries

subKeyDict = dict(zip(subKeys, subLocs))

dataEntries = dict()
for key in subKeys:
    dataEntries[key] = []

counter = 0 
with open('nlsy97_all_1997-2013.dat') as fin:
    csvReader = csv.reader(fin, delimiter = ' ', quoting = csv.QUOTE_NONE)
    for row in csvReader:
        for key in subKeyDict:
            dataEntries[key].append(row[subKeyDict[key]])
        counter += 1
        if counter % 1000 == 0:
            print(counter, 'done')

with open('nlsy97_demographicBMI.json', 'w') as fout:
    json.dump(dataEntries, fout, indent = 4)
    fout.write('\n')
