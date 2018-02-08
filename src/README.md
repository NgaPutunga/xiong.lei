# Xiong Lei, 2/7/2018

Please run this code by Python 3.0 or later version

I tested it for 2014-2015 dateset 1.3GB, it takes me about 500 sec.

Ideas of codes:
1. Use regex to extract the data as groups of ID, name, one line by one line ...
2. Simutaneously, if the extract line is valid, then Change the name s.upper() to uppercase just in case the data is not formated as uppercase; set a tmp variable to get the current year.
3. Construct a dictionary with key = NAME + ZIPCODE, e.g. "XIONG, LEI16803", and the value is an updated list of useful information for that donor, the information is a tuple containing multiple elements such as ID, name...; Among them the repeat donor which parses by key would have multiple tuples/elements of the list, which indicates the repeat donor contributes multiple times in the current year.
4. Pick up the donation by whom donated both previous year and this year; and eliminate the previous-year donation, keeping the repeat donor.
5. calculation the summatoin, percentiles for each recipient at same zipcode and calendar year.
6. write output file a the same time

     I am very excited to take part in this challenge. Appreciate it. Thank you for your time and consideration. Hope to have opportunity to further discuss my qualification.    Xiong Lei, 2/7/2018
