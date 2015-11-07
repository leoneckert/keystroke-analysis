# to work with csv files:
import csv
# in order to pass arguments from the command line:
import sys
# to make tests
from random import randint
# for settings file
import ConfigParser


def retrieveRelevantLines(dataPath):

	data = open(dataPath, "rU")

	usefulData = [] # in this array we will format the data to our wishes
	
	for row in data:
		splitrows = row.split(",")  # putting the lines from the log file into the array.
		if len(splitrows) == 3:		# Making sure only the useful lines (not the data when log was started etc) are included.

			if (splitrows[2] == "\n"):			# i dont know why the keylogger sometimes records " ". Must be [space], and sometimes "",
				splitrows[2] = "[space]\n"		# for now I replace this both with spacebut will change the keylogger script to make that more clear
			
			usefulData.append(splitrows)
	
	count = 0  #for printing documentation purpose

	for i in range(len(usefulData)):
		count = count + 1
		usefulData[i][2] = usefulData[i][2].replace("\n", "")			# here I remove the line break after each keystroke value
		usefulData[i][2] = usefulData[i][2].replace(" ", "[space]")		# and also change the space value to be represented as "[space]" instead of " "
		
	if printInfo:
		print ""
		print "[+] RETRIEVED USEFUL DATA from the input file."
		print "    -> number of valid keystrokes: " + str(count)
		print ""

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
				
	if printInfo: 
		count1 = 0  # double checking
		for i in range(len(usefulData)):
			if len(usefulData[i][1]) == 9:
				count1 = count1 + 1
		print ""
		print "[+] in " + str(count) + " instances the value for 'nanoseconds' was smaller than 9 digits" 
		print "    -> after prepending zeros, the number of instances with exactly 9 digits is " + str(count1)
		print ""

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
	
	if printInfo:
		print ""
		print "[+] I merged seconds and nanosecond " + str(count) + " times and decreased the length of the arrays."
		print "    -> a randomly chosen example array is: " + str(usefulData[randint(0, len(usefulData))])
		print ""

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


	if printInfo:
		r = randint(0, len(dictionairies))   # documentation print purpose
		iterator = 0
		randomKey = usefulData[0][1] #initialize value, changed at random in for loop below
		for key in dictionairies:
			if iterator == r:
				randomKey = key
			iterator = iterator + 1
		print "" 
		print "[+] I created a Main Dictionairy (MD). The number of entries is " + str(countDicts)
		print "    -> a randomly chosen MD entry is: key >> \"" + str(randomKey) + "\"   value >> \"" + str(dictionairies[randomKey]) + "\""
		printNumberMDentries(dictionairies)
		printNumberKEYentries(dictionairies)
		printNumberDurationValues(dictionairies)
		print ""
	
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

	if printInfo:
		r = randint(0, len(dictionairies)) # documentation print purpose
		iterator = 0
		randomKey = usefulData[0][1] #initialize value, changed at random in for loop below
		for key in dictionairies:
			if iterator == r:
				randomKey = key
			iterator = iterator + 1
		print ""
		# print ("/ " * 60 + "\n" + "\ " * 60 + "\n")*2 + "above we fill the actual data, the duration it takes between two letters into the arrays inside the dicionaires inside the dictionairy" + ("\n" + "/ " * 60 + "\n" + "\ " * 60)* 2
		print "[+] inside the dictionairies in the MD, I created a total of " + str(countEntries) + " keys."
		print "[ ] each key holds the DURATION values that it took to type the MD-key and the corresponding other key."
		print "    -> a randomly chosen MD entry is now: key >> \"" + str(randomKey) + "\"   value >> \"" + str(dictionairies[randomKey]) + "\""
		printNumberMDentries(dictionairies)
		printNumberKEYentries(dictionairies)
		printNumberDurationValues(dictionairies)		
		print ""

	return dictionairies


def removeLongDurations(dictionairies, threshold):  #threshold in seconds
	if printInfo: 
		print ""
		print "[+] IMPORTANT STEP:"
		print "[ ] We will now go through all duration values and remove the ones bigger than the set threshold of " + str(threshold) + " seconds."
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
				dictionairies[i].pop(j, None)   # and here again with empty array

		for j in dictionairies[i]:
			if dictionairies[i].get(j) == []:
				print "STILL EMPTY!"


	if printInfo:
		print "   -> looked through " + str(counti) + " MD entries."
		print "   -> looked through a total of " + str(countj) + " KEY entries in these MD entries."
		print "   -> inspected " + str(countk) + " duration values in these KEY entries and found " + str(countTooBig) + " duration values that were bigger than " + str(threshold) + " seconds."
		print "   -> after removing these duration values, I was left with " + str(countEmptyArray) + " empty duration value arrays of KEY entries"
		print "   -> I then removed " + str(countEmptyArray) + " KEY entries, that were left empty after rmoving the too big values"
		counti = 0
		countj = 0
		countk = 0
		countTooBig = 0
		countEmptyArray = 0
		for i in dictionairies:
			# print i
			counti = counti + 1

			for j in dictionairies[i]:
				# print "    " + str(j) 
				countj = countj + 1
				# print "              " + str(dictionairies[i].get(j))
				if dictionairies[i].get(j) == []:
					countEmptyArray = countEmptyArray +1
				for k in dictionairies[i].get(j):
					# print "              " + str(k)
					countk = countk + 1

		print "        -> " + str(counti) + " MD entries"
		print "        -> " + str(countj) + " KEY entries in these MD entries"
		print "        -> " + str(countk) + " duration values in these KEY entries"
		print "        -> " + str(countEmptyArray) + " duration value arrays in these KEY entries"
		print "        -> " + str(countTooBig) + " durations that were bigger than " + str(threshold) + " seconds."
		print ""


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

	if printInfo: 
		print ""
		print "[+] In " + str(countLongArrays) + " duration value arrays, there was more than 1 value."
		print "[ ] In all those cases, took the average of all the values, and set this as the duration value array's only value."
		if floatType == True:
			print "[ ] Data type of the average values: float (this can be modified in the settings)."
		else:
			print "[ ] Data type of the average values: integer (this can be modified in the settings)."
		printNumberMDentries(dictionairies)
		printNumberKEYentries(dictionairies)
		printNumberDurationValues(dictionairies)
		print ""

	return dictionairies	

def createDataArrayOfArrays(dictionairies, allKeyStrokes, timeConversion, floatType):

	#into the array we dont put any header values, we only need the allKeyStrokes array to get its length
	keyStrokeLengths = len(allKeyStrokes)

	outPutArray = []

	# this seems to make life a little easier, and sorts the keys in the same order 
	# as the values in allKeyStrokes (which is important later when exporting or printing the result)
	sorteddict = []
	for key in dictionairies:
		sorteddict.append(key)

	# now we go through rows and columns and fille in the data we got
	for i in range(keyStrokeLengths):
		# a tempArray for each row, appending it to the overall array in the end
		tempArray = []
		# checking if they key we inspect in that row is in our dictionairies array
		if allKeyStrokes[i] in sorteddict:
			# if yes we go through every column and check if the correspinding jey is in the dictioaniry of that key in the main dictionairy we are currently inspecting
			for j in range(keyStrokeLengths):
				# if yes, we append the value connected to that key.
				if allKeyStrokes[j] in dictionairies.get(allKeyStrokes[i]):
					if floatType == True:
						timeInNano = float(dictionairies.get(allKeyStrokes[i]).get(allKeyStrokes[j])[0])
					else:
						timeInNano = dictionairies.get(allKeyStrokes[i]).get(allKeyStrokes[j])[0]

					tempArray.append((timeInNano/timeConversion))
				else:
					tempArray.append("-")
		else:
			#if a key the is inpsected in a row is not in the main dictioaniry, we just print "-" for the whole row
			for j in range(keyStrokeLengths):
				tempArray.append("-")
	
		# after filleing the temoArray for the while row, we append it to the official outPutArray
		outPutArray.append(tempArray)
	if printInfo:
		print ""
		print "[+] created an output array that carries one array for each KEY entries holding all the average duration values an '-' where no record has been made."
		if floatType == True:
			print "[ ] Data type of the duration values: float (this can be modified in the settings)."
		else:
			print "[ ] Data type of the duration values: integer (this can be modified in the settings)."
		print ""
	# this is the product of all above calculation
	# below further function to format, present and export this product in different ways
	return outPutArray

def printMinAndMaxValue(outPutArray):
	maxim = 0
	for i in outPutArray:
		for j in i:
			if j > maxim and j != "-":
				maxim = j
	minim = maxim
	for i in outPutArray:
		for j in i:
			if j < minim and j != "-":
				minim = j
	if outPutArraryTimeFormat == 1:
		format = 'nanoseconds'
	elif outPutArraryTimeFormat == 1000:
		format = 'microseconds'
	elif outPutArraryTimeFormat == 1000000:
		format = 'milliseconds'
	elif outPutArraryTimeFormat == 1000000000:
		format = 'nanoseconds'
	else:
		format = 'time format: undefined'
	print ""
	print "[+] The HIGHEST value in the outPutArray is: " + str(maxim) + " (" + format + ")"
	print "[+] The LOWEST value in the outPutArray is: " + str(minim) + " (" + format + ")"
	print ""




def printTableToTerminal(outPutArray, allKeyStrokes):
	
	row_format ="{:>15}" * (len(allKeyStrokes) + 1)
	print row_format.format("", *allKeyStrokes)
	for key, row in zip(allKeyStrokes, outPutArray):
   		print row_format.format(key, *row)


def saveToCsv(outPutArray, allKeyStrokes, outFile):
	
	c = csv.writer(open(outFile, "wb"))

	tempArray = []
	tempArray.append("")
	for i in allKeyStrokes:
		tempArray.append(i)
	
	c.writerow(tempArray)
	
	for i in range(len(allKeyStrokes)):
		tempValueArray = []
		tempValueArray.append(allKeyStrokes[i])
		for j in range(len(allKeyStrokes)):
			tempValueArray.append(outPutArray[i][j])
		c.writerow(tempValueArray)


def printNumberMDentries(dictionairies):
	counti = 0
	for i in dictionairies:
		counti = counti + 1
	print "        -> " + str(counti) + " MD entries"
	
def printNumberKEYentries(dictionairies):
	countj = 0
	for i in dictionairies:
		for j in dictionairies[i]:
			countj = countj + 1		
	print "        -> " + str(countj) + " KEY entries in these MD entries"

def printNumberDurationValues(dictionairies):
	countk = 0
	for i in dictionairies:
		for j in dictionairies[i]:
			for k in dictionairies[i].get(j):
				countk = countk + 1			
	print "        -> " + str(countk) + " duration values in these KEY entries"




# THESE ARE DEFAULT SETTING, change them in the settings file
printInfo = True
outPutArraryTimeFormat = 1 
outPutArrayFloatType = False 
printTableToTerminalSetting = False
maxSecondsBetweenKeyStrokes = 2



def Main():
	# run script like this: 
	# 			python keystroke_analysis.py keystrokes.csv
	#
	# in order to export to file run like this:
	# 			python keystroke_analysis.py keystrokes.csv outFile.csv

	#declaring as global so we can change through settings
	global printInfo
	global outPutArraryTimeFormat
	global outPutArrayFloatType
	global printTableToTerminalSetting
	global maxSecondsBetweenKeyStrokes

	# first reading the settings
	config = ConfigParser.ConfigParser()
	try:
		config.read('settings.cfg')
		if (config.get('settings','printInfo') == 'False'):
			printInfo = False
		outPutArraryTimeFormat = int(config.get('settings','outPutArraryTimeFormat'))
		if (config.get('settings','outPutArrayFloatType') == 'True'):
			outPutArrayFloatType = True
		if (config.get('settings','printTableToTerminalSetting') == 'True'):
			printTableToTerminalSetting = True
		maxSecondsBetweenKeyStrokes = int(config.get('settings','maxSecondsBetweenKeyStrokes'))

		if printInfo:
			print "[+] Read settings"
	except:
		print "[-] Could not read settings"

	
	file_to_analyse = sys.argv[1]

	usefulData = retrieveRelevantLines(file_to_analyse)

	usefulData = addZerosToNanoseconds(usefulData)
	usefulData = mergeTimestampsToNanoseconds(usefulData)

	dictionairies = createDictionairies(usefulData)
	dictionairies = fillAllDictionairiesWithData(usefulData, dictionairies)

	dictionairies = removeLongDurations(dictionairies, maxSecondsBetweenKeyStrokes) #threshold value in seconds
	dictionairies = replaceMultipleDurationByAverage(dictionairies, outPutArrayFloatType)

	allKeyStrokesFromScript = ["a","s","d","f","h","g","z","x","c","v","b","q","w","e","r","y","t","1","2","3","4","6","5","=","9","7","-","8","0","]","o","u","[","i","p","l","j","'","k",",","\\",",","/","n","m",".","`","[decimal]","[asterisk]","[plus]","[clear]","[divide]","[enter]","[hyphen]","[equals]","0","1","2","3","4","5","6","7","8","9","[return]","[tab]","[space]","[del]","[esc]","[cmd]","[shift]","[caps]","[option]","[ctrl]","[shift]","[option]","[ctrl]","[fn]","[f17]","[volup]","[voldown]","[mute]","[f18]","[f19]","[f20]","[f5]","[f6]","[f7]","[f3]","[f8]","[f9]","[f11]","[f13]","[f16]","[f14]","[f10]","[f12]","[f15]","[help]","[home]","[pgup]","[fwddel]","[f4]","[end]","[f2]","[pgdown]","[f1]","[left]","[right]","[down]","[up]"]
	allKeyStrokes = []
	#making sure we dont include double values and bringing the strokes in alphabetical order:
	for i in sorted(allKeyStrokesFromScript):
		if i not in allKeyStrokes:
			allKeyStrokes.append(i)


	outArray = createDataArrayOfArrays(dictionairies, allKeyStrokes, outPutArraryTimeFormat, outPutArrayFloatType) 
	if printInfo:
		printMinAndMaxValue(outArray)

	if printTableToTerminalSetting:
		printTableToTerminal(outArray, allKeyStrokes)

	try:
		if(sys.argv[2]):
			outFile = sys.argv[2]
			saveToCsv(outArray, allKeyStrokes, outFile)

	except:
		print ""

if __name__ == '__main__':
	Main()

