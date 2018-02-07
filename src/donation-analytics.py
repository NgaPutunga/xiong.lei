
import re
from collections import defaultdict
import numpy as np
inputfile = "./input/itcont.txt"
outputfile = './output/repeat_donors.txt'
parafile = "./input/percentile.txt"

with open(parafile,'r') as f:  # read input file
    for line in f:
        Per = int(line.rstrip())
     
d = defaultdict(list)
date = 0  # initial year
with open(inputfile,'r') as i:  # read input file
    for line in i:
        donation = line.rstrip()
        donlist = donation.split('|')
        if donlist[15] == '' and \
        re.match("^(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(19|20)\d\d$", donlist[13]) and \
        re.match("^\d{5}(?:\d{4})?$", donlist[10]) and  \
        re.match(r'[a-zA-Z,\.\s]+$', donlist[7]) and \
        donlist[0] != '' and donlist[14] != '':  # parse the format of each line
            name = donlist[7].upper()  # in case the name is lowercase
            zipcode = donlist[10][0:5]  # extrac first 5 digit of zipcode
            info = (donlist[0], name, zipcode, donlist[13], donlist[14])  # tuple for CMTE_ID, name, zipcode ...
            d[name+zipcode].append(info) # make a dict with value as a list of tuple of the required information
            tmp = int(donlist[13][4:]) # tmperary variable for calender year
            if tmp > date:
                date = tmp # identify current calender year

lines = []
amt = defaultdict(list)
for key, val in d.items(): # iterate each donor     
    if all(c in [int(elm[3][4:]) for elm in val] for c in (date, date-1)):  # Identify repeat donor, who donates this year after previous year donation
        for x in val: 
            if int(x[3][4:]) == date:  # only take the current year value
                amt[x[0]].append(int(x[4])) # make a dict of list to store each recipent
                amtarr = np.array(amt[x[0]])
                amtsum = sum(amt[x[0]])
                p = int(round(np.percentile(amtarr, Per, interpolation='nearest')+1e-15)) # round up
                lines.append("|".join([x[0], x[2], x[3][4:], str(p), str(amtsum), str(len(amt[x[0]]))])) 

# write output file
with open(outputfile,'w') as o:
    for line in lines:
        o.write("%s\n" % line)