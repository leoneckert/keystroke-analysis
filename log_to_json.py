# to work with csv files:
import csv
# in order to pass arguments from the command line:
import sys

import json
from pprint import pprint

def retrieveRelevantLines(dataPath):

	data = open(dataPath, "rU")

	usefulData = [] # in this array we will format the data to our wishes
	
	for row in data:
		splitrows = row.split(",")  # putting the lines from the log file into the array.
		if len(splitrows) == 3 and splitrows[2] != "[unknown]\n":		# Making sure only the useful lines (not the data when log was started etc) are included.			
			usefulData.append(splitrows)
		if len(splitrows) == 4: #split works funnily if the key is a ',' itself, here is the fix:
			splitrows.pop()
			splitrows[2] = ','
			usefulData.append(splitrows)
	
	count = 0  #for printing documentation purpose

	for i in range(len(usefulData)):
		count = count + 1
		usefulData[i][2] = usefulData[i][2].replace("\n", "")			# here I remove the line break after each keystroke value
		
	# if printInfo:
	# 	print ""
	# 	print "[+] RETRIEVED USEFUL DATA from the input file."
	# 	print "    -> number of valid keystrokes: " + str(count)
	# 	print ""
	
	# print usefulData

	return usefulData

def addZerosToNanoseconds(usefulData):	
	# some values in the nanosecond section are below 9 digits long, 
	# here I add to zeros to the beginning if that the case to make them all equal.
	count = 0 	#for printing documentation purpose
	
	for i in range(len(usefulData)):
		if len(usefulData[i][1]) < 9:
			count = count + 1
			missingDigits = 9 - len(usefulData[i][1])
			for j in range(missingDigits):
				usefulData[i][1] = str(0) + usefulData[i][1]
				
	# if printInfo: 
	# 	count1 = 0  # double checking
	# 	for i in range(len(usefulData)):
	# 		if len(usefulData[i][1]) == 9:
	# 			count1 = count1 + 1
	# 	print ""
	# 	print "[+] in " + str(count) + " instances the value for 'nanoseconds' was smaller than 9 digits" 
	# 	print "    -> after prepending zeros, the number of instances with exactly 9 digits is " + str(count1)
	# 	print ""

	return usefulData	


def mergeTimestampsToNanoseconds(usefulData):
	# now I merge seconds and nanoseconds, so together they are just one nano second value
	# every data entry is therefore only 2 elements long, one for the nanoseconds, one for the keystroke value
	count = 0  #printing documentation purposes
	for i in range(len(usefulData)):
		usefulData[i][0] = usefulData[i][0] + usefulData[i][1]
		count = count + 1
		usefulData[i][1] = usefulData[i][2]
		usefulData[i].pop()  #taking out the last value [2] that we dont need anymore
	
	# if printInfo:
	# 	print ""
	# 	print "[+] I merged seconds and nanosecond " + str(count) + " times and decreased the length of the arrays."
	# 	print "    -> a randomly chosen example array is: " + str(usefulData[randint(0, len(usefulData))])
	# 	print ""

	return usefulData

def createDictionairies(usefulData):
	# now all the entries are in the format we want them and we are ready to make sense of them
	# i make a Main Dictionairy (MD) that itself will hold dictionairies for every key (KEY dictionairy)
	# in the ditcionairy for each letter, there will be keys, for each letter and arrays of values that tell the duration it took to get from the dict letter to the key letter
	# dictionairies = { "a" = {"a" : [duration1, duration2, duration3, ...]; "b" : [duration1, ...]; ...}; "b" = {"a" : [duration1, duration2, duration3, ...] ...}         }
	dictionairies = {}
	countDicts = 0  # documentation print purpose

	for i in range(len(usefulData)):
		if usefulData[i][1] not in dictionairies: #iterating through all keys pressed and checking if they are in the MD already.
			dictionairies[usefulData[i][1]] = {}
			countDicts = countDicts + 1


	# if printInfo:
	# 	r = randint(0, len(dictionairies))   # documentation print purpose
	# 	iterator = 0
	# 	randomKey = usefulData[0][1] #initialize value, changed at random in for loop below
	# 	for key in dictionairies:
	# 		if iterator == r:
	# 			randomKey = key
	# 		iterator = iterator + 1
	# 	print "" 
	# 	print "[+] I created a Main Dictionairy (MD). The number of entries is " + str(countDicts)
	# 	print "    -> a randomly chosen MD entry is: key >> \"" + str(randomKey) + "\"   value >> \"" + str(dictionairies[randomKey]) + "\""
	# 	printNumberMDentries(dictionairies)
	# 	printNumberKEYentries(dictionairies)
	# 	printNumberDurationValues(dictionairies)
	# 	print ""
	
	return dictionairies

def fillAllDictionairiesWithData(usefulData, dictionairies):
	# now the KEY dictionairies inside the MD are ready to be filled
	# i'll explain on the example of the dictionairy for the letter/key "a"
	# the a-dictionairy stores keys for every key that were pressed in succession to a. 
	# as values for these keys stands an array storing the the duration (in nanoseconds) that passed between typing a and the key-letter letter
	# the last value in the log does not have a succeeding keystroke, therefore the -1
	countEntries = 0
	for i in range(len(usefulData)-1): 
		if usefulData[i+1][1] not in dictionairies.get(usefulData[i][1]): #checking if a key is part of a KEY entry inside MD already
			dictionairies.get(usefulData[i][1])[usefulData[i+1][1]] = [] #if not we add a new entry in side a KEY entry and give an ampty array as a value
			countEntries = countEntries + 1

		#then we ad the difference betwween the next timestamp and the currently inspected one:
		dictionairies.get(usefulData[i][1])[usefulData[i+1][1]].append(int(usefulData[i+1][0]) - int(usefulData[i][0])) 

	# if printInfo:
	# 	r = randint(0, len(dictionairies)) # documentation print purpose
	# 	iterator = 0
	# 	randomKey = usefulData[0][1] #initialize value, changed at random in for loop below
	# 	for key in dictionairies:
	# 		if iterator == r:
	# 			randomKey = key
	# 		iterator = iterator + 1
	# 	print ""
	# 	# print ("/ " * 60 + "\n" + "\ " * 60 + "\n")*2 + "above we fill the actual data, the duration it takes between two letters into the arrays inside the dicionaires inside the dictionairy" + ("\n" + "/ " * 60 + "\n" + "\ " * 60)* 2
	# 	print "[+] inside the dictionairies in the MD, I created a total of " + str(countEntries) + " keys."
	# 	print "[ ] each key holds the DURATION values that it took to type the MD-key and the corresponding other key."
	# 	print "    -> a randomly chosen MD entry is now: key >> \"" + str(randomKey) + "\"   value >> \"" + str(dictionairies[randomKey]) + "\""
	# 	printNumberMDentries(dictionairies)
	# 	printNumberKEYentries(dictionairies)
	# 	printNumberDurationValues(dictionairies)		
	# 	print ""


	return dictionairies

def removeLongDurations(dictionairies, threshold):  #threshold in seconds
	# if printInfo: 
	# 	print ""
	# 	print "[+] IMPORTANT STEP:"
	# 	print "[ ] We will now go through all duration values and remove the ones bigger than the set threshold of " + str(threshold) + " seconds."
	# before we calculate the average value of each key change, we remove values above a certain threshold (in seconds), as people make longer pauses that 
	# would confuse they value of the data
	counti = 0    #this step took me longer  time to get workking perfectly. Went through many correction and debugging. Hence very precise printing and inspection
	countj = 0
	countk = 0
	countTooBig = 0
	countEmptyArray = 0

	for i in dictionairies:
		counti = counti + 1
		keyValuePairNeedToRemove = []  # this turned out to be the best way to collect entries that are to be later deletd (after iterating through them)

		for j in dictionairies[i]:
			countj = countj + 1
			durationsNeedToRemove = []  #same concept here, first collect....

			for k in dictionairies[i].get(j):

				countk = countk + 1

				if (k/1000000000 > int(threshold)-1):  #-1 because if the value is 0, it returns all times under 1 second
					countTooBig = countTooBig + 1

					durationsNeedToRemove.append(k)  #...collecting here
			
			if durationsNeedToRemove != []:   #then, if entries to delete have been found...
				for k in durationsNeedToRemove:
					dictionairies[i].get(j).remove(k)  #...delete them, here the values that are to big
			
			if dictionairies[i].get(j) == []:
				countEmptyArray = countEmptyArray + 1
				keyValuePairNeedToRemove.append(j)    
		
		if keyValuePairNeedToRemove != []:
			for j in keyValuePairNeedToRemove:
				dictionairies[i].pop(j, None)   # and here again with empty array.

		for j in dictionairies[i]:
			if dictionairies[i].get(j) == []:
				print "STILL EMPTY!"

	# and here we remove empty key value pairs in dictionairy 
	firstLevelKeysToRemove = []
	for i in dictionairies:
		if dictionairies[i] == {}:
			firstLevelKeysToRemove.append(i)
	for i in range(len(firstLevelKeysToRemove)):
		dictionairies.pop(firstLevelKeysToRemove[i], None)   # and here again with empty array


	# if printInfo:
	# 	print "   -> looked through " + str(counti) + " MD entries."
	# 	print "   -> looked through a total of " + str(countj) + " KEY entries in these MD entries."
	# 	print "   -> inspected " + str(countk) + " duration values in these KEY entries and found " + str(countTooBig) + " duration values that were bigger than " + str(threshold) + " seconds."
	# 	print "   -> after removing these duration values, I was left with " + str(countEmptyArray) + " empty duration value arrays of KEY entries"
	# 	print "   -> I then removed " + str(countEmptyArray) + " KEY entries, that were left empty after rmoving the too big values"
	# 	counti = 0
	# 	countj = 0
	# 	countk = 0
	# 	countTooBig = 0
	# 	countEmptyArray = 0
	# 	for i in dictionairies:
	# 		# print i
	# 		counti = counti + 1

	# 		for j in dictionairies[i]:
	# 			# print "    " + str(j) 
	# 			countj = countj + 1
	# 			# print "              " + str(dictionairies[i].get(j))
	# 			if dictionairies[i].get(j) == []:
	# 				countEmptyArray = countEmptyArray +1
	# 			for k in dictionairies[i].get(j):
	# 				# print "              " + str(k)
	# 				countk = countk + 1

	# 	print "        -> " + str(counti) + " MD entries"
	# 	print "        -> " + str(countj) + " KEY entries in these MD entries"
	# 	print "        -> " + str(countk) + " duration values in these KEY entries"
	# 	print "        -> " + str(countEmptyArray) + " duration value arrays in these KEY entries"
	# 	print "        -> " + str(countTooBig) + " durations that were bigger than " + str(threshold) + " seconds."
	# 	print ""


	return dictionairies

def replaceMultipleDurationByAverage(dictionairies, floatType):
	# condense arrays with multiple duration values down to their average:
	countLongArrays = 0			#docu purposes
	for i in dictionairies.values():
		for j in i.values():
			if len(j) > 1:
				countLongArrays = countLongArrays + 1  #docu purposes
	
				arrayLength = len(j)
				valueSum = 0
				for k in range(arrayLength):  #adding all the values in one array up
					valueSum = valueSum + j[k]
				if floatType == True:
					averageValue = float(valueSum)/arrayLength  #then taking the avergae
				else:
					averageValue = valueSum/arrayLength  #then taking the avergae
				

				for k in range(arrayLength - 1):  #popping all, but one value out of the array
					j.pop()
	
				j[0] = averageValue  #and replacing the last remaingin one by the average value calculated

	# if printInfo: 
	# 	print ""
	# 	print "[+] In " + str(countLongArrays) + " duration value arrays, there was more than 1 value."
	# 	print "[ ] In all those cases, took the average of all the values, and set this as the duration value array's only value."
	# 	if floatType == True:
	# 		print "[ ] Data type of the average values: float (this can be modified in the settings)."
	# 	else:
	# 		print "[ ] Data type of the average values: integer (this can be modified in the settings)."
	# 	printNumberMDentries(dictionairies)
	# 	printNumberKEYentries(dictionairies)
	# 	printNumberDurationValues(dictionairies)
	# 	print ""
 
	return dictionairies	

def convertStringsToKeyCode(dictionairies):
	with open('allKeysLogged.json', 'r') as allKeys:
		keysLogged = json.load(allKeys)
	# for i in dictionairies:
	# 	print i
	# 	if i in keysLogged:
	# 		# print keysLogged[i]
	# 		# print "NOOOOOOO"
	# 		# i = keysLogged[i]
	# 		dictionairies[keysLogged[i]] = dictionairies.pop(i)
	for i in keysLogged:
		# print i
		if i in dictionairies:
			# print "yes"
			# print i 
			# print keysLogged[i]
			dictionairies[keysLogged[i]] = dictionairies.pop(i)
	for i in dictionairies:
		# print i
		# print dictionairies[i]
		for j in keysLogged:
			# print j
			if j in dictionairies[i]:
				# print j
				dictionairies[i][keysLogged[j]] = dictionairies[i].pop(j)
		# print i
		# print dictionairies[i]

	# print"------"
	# for i in dictionairies:
	# 	print i
	return dictionairies
	

def Main():	
	file_to_analyse = sys.argv[1]
	usefulData = retrieveRelevantLines(file_to_analyse)
	usefulData = addZerosToNanoseconds(usefulData)
	usefulData = mergeTimestampsToNanoseconds(usefulData)
	dictionairies = createDictionairies(usefulData)
	dictionairies = fillAllDictionairiesWithData(usefulData, dictionairies)
	dictionairies = removeLongDurations(dictionairies, 1)
	accuracy = 0
	for i in dictionairies:
		# print i
		for j in dictionairies[i]:
			# print"   "+ j
			for k in dictionairies[i][j]:
				# print "      " + str(k)
				accuracy = accuracy + 1
	dictionairies = replaceMultipleDurationByAverage(dictionairies, True)
	dictionairies = convertStringsToKeyCode(dictionairies)
	

	
	# for i in dictionairies:
	# 	print i, dictionairies[i]



	# # print as json
	# #!! in the end i will have to replace though keyCodes!
	output = {}
	output['accuracy'] = accuracy
	output['data'] = dictionairies
	
	json_data = json.dumps(dictionairies) # change this to "output" in the brakcets once accuracy is supported
	parsed = json.loads(json_data)
	print json.dumps(parsed, indent=4, sort_keys=True)
	with open('myCompressedKeyprint.json', 'w') as outfile:
		json.dump(parsed, outfile, indent=4, sort_keys=True)
		


if __name__ == '__main__':
	Main()