
import re
from collections import defaultdict
import numpy as np
import time
import sys

inFile1 = sys.argv[1]
inFile2 = sys.argv[2]
outFile = sys.argv[3]
start_time = time.clock()

with open(inFile2,'r') as f:  # read input file
    for line in f:
        Per = int(line.rstrip())
     
d = defaultdict(list)  # dict for each donor
date = 0  # initial year
lines = []  # output string
amt = defaultdict(list)  # initial amount of donation

def dict_donator(CMTE_ID, name, zipcode, Tran_DT, Tran_AMT): # dictionary construction
    d[name+zipcode].append((CMTE_ID, name, zipcode, Tran_DT, Tran_AMT))

with open(inFile1,'r') as i:  # read input file
    with open(outFile,'a+') as o: # write out file
        for line in i:  # data streams in
            donation = line.rstrip() # get rid of "\n"
            donlist = donation.split('|')
            if donlist[15] == '' and \
            re.match(r"^(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(19|20)\d\d$", donlist[13]) and \
            re.match(r"^\d{5}(?:\d{4})?$", donlist[10]) and  \
            re.match(r'[a-zA-Z,\.\s]+$', donlist[7]) and \
            re.match(r"^\w{9}$", donlist[0])  and \
            re.match(r"(?=(\d\.?){1,14}$)\d+(\.\d{1,2})?$", donlist[14]):  # parse the format of each line [Other_ID, Tran_DT, zipcode, name, CMET_ID, Tran_AMT]
            # dictionary construction
                name = donlist[7].upper()  # in case the name is lowercase
                zipcode = donlist[10][0:5]  # extrac first 5 digit of zipcode
                dict_donator(donlist[0], name, zipcode, donlist[13], donlist[14])  # make a dict with value as a list of tuple of the required information
                date = int(donlist[13][4:]) # current processing calender year
            # start to process   
                if any([int(elm[3][4:]) < date for elm in d[name+zipcode]]):  # Identify repeat donor, who donates this year after previous year donation, note: the d.values() provides a list of all donors, but we care about current single donor.
                # elm is every five key info. of a donor' contribution
                    for x in d[name+zipcode]: 
                        if int(x[3][4:]) == date:  # only take the current year value
                            key_rep = x[0]+x[2]+x[3][4:]  # key for recepient
                            amt[key_rep].append(int(x[4])) # make a dict of list to store each recipient
                            amtarr = np.array(amt[key_rep])
                            amtsum = sum(amt[key_rep])
                            p = int(round(np.percentile(amtarr, Per, interpolation='nearest')+1e-15)) # round up
                            out = ("|".join([x[0], x[2], x[3][4:], str(p), str(amtsum), str(len(amt[key_rep]))]))
                            o.write("%s\n" % out)
print ("time consuming: ", time.clock() - start_time,"s")  