""" Alluvial plots for one-step lookaheads on weight transitions. Separate by sex 
    Only plot ages 12-30, as edges are more sparse. """

import json, plotly
import pandas as pd 
import numpy as np
import setup_nlsy97Analysis as util

strataList = ['Obese', 'Overweight', 'Normal', 'Underweight']
colorList = ['#CA0020', '#F4A582', '#FFFFFF', '#92C5DE']
countFile = 'weightTransitionCounts.json'
normalizeCountFile = 'normalizedWeightTransitions.json'

def main(strataList, colorList, countFile, normalizeCountFile):

    with open(countFile, 'r') as fin:
        data = json.load(fin)

    ageSort = []
    for age in data['M']:
        ageSort.append(int(age))
    ageSort = sorted(ageSort)[0:-2] #30 cutoff

    femaleSankDF = util.createSankeyDF(data, ageSort, gender = 'F',
        strataList = strataList, colorList = colorList)
    util.makeSankey(femaleSankDF, label = 'Strata', 
        plotTitle = 'BMI strata mobility - Females, ages 12-30', 
        fileName = 'Results/Figure1.html')
    
    maleSankDF = util.createSankeyDF(data, ageSort, gender = 'M', 
        strataList = strataList, colorList = colorList)
    util.makeSankey(maleSankDF, label = 'Strata', 
        plotTitle = 'BMI strata mobility - Males, ages 12-30', 
        fileName = 'Results/Figure2.html')
    
    with open(normalizeCountFile, 'r') as fin: #Try normalizeds
        normData = json.load(fin)

    femaleSankDF = util.createSankeyDF(normData, ageSort, gender = 'F', 
        strataList = strataList, colorList = colorList)
    util.makeSankey(femaleSankDF, label = 'Strata', 
        plotTitle = 'Normalized BMI strata mobility - Females, ages 12-30', 
        fileName = 'Results/Figure3.html')
    
    maleSankDF = util.createSankeyDF(normData, ageSort, gender = 'M', 
        strataList = strataList, colorList = colorList)
    util.makeSankey(maleSankDF, label = 'Strata', 
        plotTitle = 'Normalized BMI strata mobility - Males, ages 12-30', 
        fileName = 'Results/Figure4.html')
    
if __name__ == '__main__':

    main(strataList, colorList, countFile, normalizeCountFile)