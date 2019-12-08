""" Analyze National Longitudinal Survey data, 1997-2013.

    This script takes partiuclar variables of interest, such as height, weight,
    and age, and converts those values to a time series of BMI measurements for a 
    given individual. A counting process is then performed for how many times
    an individual in one year with a given BMI status, e.g. obese, transitions to
    any other BMI status. This approach is a 'dumb' way of analyzing weight 
    trends longitudinally, not cross-sectionally, akin to modeling the weight 
    state as a Markov Chain.

    Additional .NLSY97 files were created using the NLSY97 Investigator to 
    extract height and weight for each year of study (1997-2013), and age of 
    each individual at the time of the annual participation. BMI was calculated
    for children using the CDC's guidelines.

    Inputs: heightFeet.NLSY97, heightInches.NLSY97, weight.NLSY97, ageMonths.NLSY97, 
                nlsy97_demographicBMI.json, bmiChildrenChart.csv
    Outputs: weightTransitionCounts.json, normalizedWeightTransitions.json

    Author: Seth Rhoades
"""
import csv, json
from scipy import stats
import pandas as pd 
import numpy as np
import setup_nlsy97Analysis as util

genderID = 'R0536300' #Gender variable ID

heightFeetKeys, heightInchesKeys, weightKeys, ageKeys =  util.readInKeys('heightFeet.NLSY97',
     'heightInches.NLSY97', 'weight.NLSY97', 'ageMonths.NLSY97')

with open('nlsy97_demographicBMI.json', 'r') as fin:
    data = json.load(fin)

individualData = util.extractVars(data, heightFeetKeys, heightInchesKeys, 
    weightKeys, ageKeys, genderID)

bmiChildren = util.prepBMIChart('bmiChildrenChart.csv')

individualDataAdd = util.addWeightStrata(individualData, bmiChildren)

transitionCounts = util.countWeightTransitions(individualDataAdd)

with open('weightTransitionCounts.json', 'w') as fout:
    json.dump(transitionCounts, fout, indent = 4)
    fout.write('\n')

weightedTransitions = util.weighTransitions(transitionCounts)

with open('normalizedWeightTransitions.json', 'w') as fout:
    json.dump(weightedTransitions, fout, indent = 4)
    fout.write('\n')
