import json, csv, plotly
import numpy as np
import pandas as pd
from scipy import stats
from itertools import chain

def readInKeys(heightFt, heightIn, weight, ageMonths):

    heightFeetKeys = []
    with open(heightFt) as fin:
        csvReader = csv.reader(fin)
        for row in csvReader:
            heightFeetKeys.append(row[0])
    heightFeetKeys = heightFeetKeys[1:]

    heightInchesKeys = []
    with open(heightIn) as fin:
        csvReader = csv.reader(fin)
        for row in csvReader:
            heightInchesKeys.append(row[0])
    heightInchesKeys = heightInchesKeys[1:]

    weightKeys = []
    with open(weight) as fin:
        csvReader = csv.reader(fin)
        for row in csvReader:
            weightKeys.append(row[0])
    weightKeys = weightKeys[1:]

    ageKeys = []
    with open(ageMonths) as fin:
        csvReader = csv.reader(fin)
        for row in csvReader:
            ageKeys.append(row[0])
    ageKeys = ageKeys[1:]

    return heightFeetKeys, heightInchesKeys, weightKeys, ageKeys


def extractVars(data, heightFeetKeys, heightInchesKeys, weightKeys, ageKeys, genderID):

    personDict = dict()
    for person in range(len(data['R0000100'])): #Base ID
        heightsFeet = []
        for heights in heightFeetKeys:
            heightsFeet.append(float(data[heights][person]))
        heightsInches = []
        for heights in heightInchesKeys:
            heightsInches.append(float(data[heights][person]))
        weights = []
        for weight in weightKeys:
            weights.append(float(data[weight][person]))
        ages = []
        for age in ageKeys:
            ages.append(float(data[age][person]))
        gender = data[genderID][person]

        if (len([x for x in heightsFeet if x < 0]) == 0 and 
            len([x for x in heightsInches if x < 0]) == 0 and
            len([x for x in weights if x < 0]) == 0 and
            len([x for x in ages if x < 0]) == 0) and gender in ['1', '2']:
            
            fullHeights = (np.array(heightsFeet) * 12) + np.array(heightsInches)
            weights = np.array(weights)
            ages = np.array(ages)
            BMIs = (weights * 703) / fullHeights**2

            personDict[person] = dict()
            personDict[person]['Height'] = fullHeights 
            personDict[person]['Weight'] = weights 
            personDict[person]['Age'] = ages
            personDict[person]['BMI'] = BMIs
            if gender == '1':
                personDict[person]['Gender'] = 'M'
            if gender == '2': 
                personDict[person]['Gender'] = 'F'
    
    return personDict


def prepBMIChart(chartFile):
    bmiChildren = pd.read_csv(chartFile)
    bmiChildren = bmiChildren[bmiChildren['Sex'] != 'Sex']
    bmiChildren['Sex'][bmiChildren['Sex'] == '1'] = 'M'
    bmiChildren['Sex'][bmiChildren['Sex'] == '2'] = 'F'
    bmiChildren['Agemos'] = bmiChildren['Agemos'].astype(float).add(0.1)
    bmiChildren['Agemos'] = np.around(bmiChildren['Agemos'])
    return bmiChildren


def addWeightStrata(individualData, childAgeChart):
    """
    Calculating bmi percentile wih children's chart:
    ... wherever gender and closest Agemos match: z-score = (((BMI/M)**L) - 1) / (L*S)
    If adult, then basic cutoffs apply, no need for math 
    Childrens chart pulled from https://www.cdc.gov/growthcharts/percentile_data_files.htm
    Note this chart goes up to 20 years of age, after that its a general cutoff
    """
    for person in individualData:
        onePerson = individualData[person]
        strata = []
        for timepoint in range(len(onePerson['Age'])):
            bmi = onePerson['BMI'][timepoint]
            if onePerson['Age'][timepoint] <= max(childAgeChart.Agemos):
                ref = childAgeChart[(childAgeChart['Sex'] == onePerson['Gender']) & 
                    (childAgeChart['Agemos'] == onePerson['Age'][timepoint])]
                zScore = ((((bmi/ref['M'].astype(float))**ref['L'].astype(float)) - 1) / 
                    (ref['L'].astype(float) * ref['S'].astype(float))).values
                percentile = stats.norm.cdf(zScore) * 100
                if len(percentile) != 1: #Might be bad gender ID?
                    percentile = np.mean(percentile)
                if percentile <= 5.:
                    strata.append('Underweight')
                elif percentile > 5. and percentile <= 85.:
                    strata.append('Normal')
                elif percentile > 85. and percentile <= 95.:
                    strata.append('Overweight')
                elif percentile > 95:
                    strata.append('Obese')
                else:
                    raise Exception('invalid percentile calculation')
            else: 
                if bmi < 18.5:
                    strata.append('Underweight')
                elif bmi >= 18.5 and bmi < 25.:
                    strata.append('Normal')
                elif bmi >= 25. and bmi < 30.:
                    strata.append('Overweight')
                elif bmi >= 30.:
                    strata.append('Obese')
                else:
                    raise Exception('invalid percentile calculation')

        individualData[person]['WeightStrata'] = strata
    return individualData


def countWeightTransitions(data, strataList = ['Underweight', 'Normal', 
    'Overweight', 'Obese']):
    """Seperate counters for males and females for age-rooted weight transitions.
    
    for each rounded age-year
    ... for each unique strata
    ... ... add to total number of strata (will be left as raw counts for now) """
    
    weightTransitions = dict()
    for person in data:

        gender = data[person]['Gender']
        if gender not in weightTransitions:
            weightTransitions[gender] = dict()

        for age in range(len(data[person]['Age'])):
            currentAge = int(data[person]['Age'][age] / 12)
            if currentAge not in weightTransitions[gender]:
                weightTransitions[gender][currentAge] = dict() 

            currentWeight = data[person]['WeightStrata'][age]
            if currentWeight not in weightTransitions[gender][currentAge]:
                weightTransitions[gender][currentAge][currentWeight] = dict() 
                weightTransitions[gender][currentAge][currentWeight]['Count'] = 0
            weightTransitions[gender][currentAge][currentWeight]['Count'] += 1
            
            if age < len(data[person]['Age']) - 1:
                nextWeight = data[person]['WeightStrata'][age + 1]
                if nextWeight not in weightTransitions[gender][currentAge][currentWeight]:
                    weightTransitions[gender][currentAge][currentWeight][nextWeight] = 0
                weightTransitions[gender][currentAge][currentWeight][nextWeight] += 1
        
        for age in weightTransitions[gender]:
            for strata in strataList:
                if strata not in weightTransitions[gender][age]:
                    weightTransitions[gender][age][strata] = dict()
                    weightTransitions[gender][age][strata]['Count'] = 0
                    for substrata in strataList:
                        weightTransitions[gender][age][strata][substrata] = 0
                else:
                    for substrata in strataList:
                        if substrata not in weightTransitions[gender][age][strata]:
                            weightTransitions[gender][age][strata][substrata] = 0

    return weightTransitions

def weighTransitions(transitionDict, normalization = 'Total'):
    """ Normalize weight transitions. Within each gender and age, a weight strata
        (e.g. "Normal") has a total count, and a count of transitions to each
        strata at age+1. The these one-to-many transitions are normalized to 1, 
        followed by the cross-sectional percentage of each strata at every age. 
        If normalization == 'Total', then the total counts for all weight strata
        at a given age is used, however is 'Weight' is used, then the counts within
        a weight strata is used as the normalization. If Total is used, then the
        normalization of each transition needs to be done against the total counts 
        at t+1, not t. """

    weightedWeights = transitionDict 
    for gender in weightedWeights:
        maxAge = max(list(weightedWeights[gender].keys()))
        for age in weightedWeights[gender]:
            if age < maxAge:
                TCsNext = 0 
                for strata in weightedWeights[gender][age + 1]:
                    TCsNext += weightedWeights[gender][age][strata]['Count']
                
                for strata in weightedWeights[gender][age]:
                    for transition in weightedWeights[gender][age][strata]:
                        if transition != 'Total':
                            if normalization == 'Weight':
                                weightedWeights[gender][age][strata][transition] = (weightedWeights[gender][age][strata][transition] / 
                                    weightedWeights[gender][age][strata]['Count']) 
                            if normalization == 'Total':      
                                weightedWeights[gender][age][strata][transition] = (weightedWeights[gender][age][strata][transition] / TCsNext)


            TCsCurrent = 0 
            for strata in weightedWeights[gender][age]:
                TCsCurrent += weightedWeights[gender][age][strata]['Count']
            
            for strata in weightedWeights[gender][age]:
                weightedWeights[gender][age][strata]['Count'] = weightedWeights[gender][age][strata]['Count'] / TCsCurrent
    
    return weightedWeights


def createSankeyDF(data, ageList, gender = 'M', strataList = ['Obese', 'Overweight', 
    'Normal', 'Underweight'], colorList = ['#CA0020', '#F4A582', '#FFFFFF', 
    '#92C5DE'], linkColors = ['rgba(202, 0, 32, 0.25)', 'rgba(0, 128, 0, 0.25)', 
    'rgba(0, 128, 0, 0.25)', 'rgba(146, 197, 222, 0.25)', 'rgba(202, 0, 32, 0.25)',
    'rgba(202, 0, 32, 0.25)', 'rgba(0, 128, 0, 0.25)', 'rgba(146, 197, 222, 0.25)',
    'rgba(202, 0, 32, 0.25)', 'rgba(202, 0, 32, 0.25)', 'rgba(0, 128, 0, 0.25)', 
    'rgba(146, 197, 222, 0.25)', 'rgba(202, 0, 32, 0.25)', 'rgba(202, 0, 32, 0.25)',
    'rgba(0, 128, 0, 0.25)', 'rgba(146, 197, 222, 0.25)'], useLinkColors = True):
    """ Make sankey plot, colors are based on repeated ordering of strata, and for
        link colors, color-coded "good/bad" transition """

    genderData = data[gender]

    #Start with creating the source and value columns 
    sankVals = []
    ageMultiplier = 0

    for age in ageList:
        ageDict = genderData[str(age)]
        sourceNum = 0
        for strata in strataList:
            source = sourceNum + (4 * ageMultiplier)
            if strata in ageDict:
                for subStrata in strataList:
                    if subStrata in ageDict[strata]:
                        destValue = ageDict[strata][subStrata]
                        sankVals.append([source, destValue, age])
            sourceNum += 1 
        ageMultiplier += 1

    sankDF = pd.DataFrame(sankVals)
    sankDF.columns = ['Source', 'Value', 'Age']
    sankDF['Target'] = 0

    for chunk in range(0, len(sankDF), 16):
        sourceVals = sankDF.Source[chunk:chunk + 16].values
        targetVals = list(set(sankDF.Source[chunk + 16: chunk + 32]))
        if len(targetVals) == 4:
            sankDF['Target'][chunk:chunk + 16] = targetVals * 4

    #Remove tail 0s for now
    sankDF = sankDF[sankDF['Target'] != 0]
    sankDF['SourceColor'] = colorList * int(len(sankDF) / 4)
    if useLinkColors == True:
        sankDF['LinkColor'] = linkColors * int(len(sankDF) / 16)
    else: #make grey80
        sankDF['LinkColor'] = ['rgba(204, 204, 204, 0.25)'] * int(len(sankDF))
    sankDF['Strata'] = strataList * int(len(sankDF) / 4)
    sankDF['Label'] = sankDF['Strata'].astype(str) + ' - Age ' + sankDF['Age'].astype(str)
    sankDF['Blank'] = ''

    return sankDF


def makeSankey(sankDF, label = 'Blank', plotTitle = 'BMI strata mobility - Males',
    fileName = 'MaleWeightSankey.html'):

    data_trace = dict(
        type = 'sankey',
        domain = dict(
        x =  [0,1],
        y =  [0,1]
        ),
        orientation = "h",
        valueformat = ".0f",
        node = dict(
            pad = 7.5,
            thickness = 8,
            line = dict(
                color = "black",
                width = 0.5
            ),
            label =  sankDF[label],
            color = sankDF['SourceColor']
        ),
        link = dict(
        source = sankDF['Source'],
        target = sankDF['Target'],
        value = sankDF['Value'],
        color = sankDF['LinkColor']
        )
    )

    layout =  dict(
        title = plotTitle,
        height = 900,
        width = 1800,
        font = dict(
        size = 14.5,
        family = 'Roboto'
        )
    )

    fig = dict(data=[data_trace], layout=layout)
    plotly.offline.plot(fig, filename = fileName)
