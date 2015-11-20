
data = open("out.csv", "rU")

outDict = ""

count = 0


allKeys = {
	"8" : "[backspace]",
	"9" : "[tab]",
	"13": "[enter]",
	"16": "[shift]",
	"17": "[ctrl]",
	"18": "[alt]",
	"20": "[caps lock]",
	"27": "[esc]",
	"32": "[space]",
	"37": "[left]",
	"38": "[up]",
	"39": "[right]",
	"40": "[down]",
	"48": "0",
	"49": "1",
	"50": "2",
	"51": "3",
	"52": "4",
	"53": "5",
	"54": "6",
	"55": "7",
	"56": "8",
	"57": "9",
	"65": "a",
	"66": "b",
	"67": "c",
	"68": "d",
	"69": "e",
	"70": "f",
	"71": "g",
	"72": "h",
	"73": "i",
	"74": "j",
	"75": "k",
	"76": "l",
	"77": "m",
	"78": "n",
	"79": "o",
	"80": "p",
	"81": "q",
	"82": "r",
	"83": "s",
	"84": "t",
	"85": "u",
	"86": "v",
	"87": "w",
	"88": "x",
	"89": "y",
	"90": "z",
	"91": "[cmd]",
	"93": "[cmd]",
	"186": ";",
	"187": "=",
	"188": ",",
	"189": "-",
	"190": ".",
	"191": "/",
	"192": "`",
	"219": "[",
	"220": "\\",
	"221": "]",
	"222": "'"
}

for key in allKeys:
	print key, allKeys[key]

arrayOfKeys = []

for row in data:
	splitrows = row.split(",")  # putting the lines from the log file into the array.
	if count == 0:
		
		for i in range(len(splitrows)):
			
			# print splitrows[i]
			arrayOfKeys.append(splitrows[i])
	else:

		tempKeyCode = "null" # this willl be a matter of changing the names in keylogger and other script.
		for key in allKeys:
			if str(splitrows[0]) == allKeys[key]:
				tempKeyCode = key
		# outDict[splitrows[0]] = {}
		if tempKeyCode != "null":
			outDict = outDict + ("\"" + str(tempKeyCode) + "\": { ")
		c_count = 0
		for i in range(len(splitrows)):
			
			if i != 0 and splitrows[i] != "-":

				tempKeyCode = "null" # this willl be a matter of changing the names in keylogger and other script.
				for key in allKeys:
					if str(arrayOfKeys[i]) == allKeys[key]:
						tempKeyCode = key
				print splitrows[i]
				print arrayOfKeys[i]
				print tempKeyCode
				if tempKeyCode != "null" and tempKeyCode != "89" and tempKeyCode != "222" :
					if c_count != 0:
						outDict = outDict + ","
					c_count = c_count + 1
					outDict = outDict + "\"" + str(tempKeyCode) + "\": [" + str(splitrows[i]) + "]"
				

		

		outDict = outDict + ("},\n")
	
	count = count + 1
print outDict


# print arrayOfKeys

	# usefulData = [] # in this array we will format the data to our wishes
	
	# for row in data:
	# 	splitrows = row.split(",")  # putting the lines from the log file into the array.
	# 	if len(splitrows) == 3:		# Making sure only the useful lines (not the data when log was started etc) are included.

	# 		if (splitrows[2] == "\n"):			# i dont know why the keylogger sometimes records " ". Must be [space], and sometimes "",
	# 			splitrows[2] = "[space]\n"		# for now I replace this both with spacebut will change the keylogger script to make that more clear
			
	# 		usefulData.append(splitrows)
	
	# count = 0  #for printing documentation purpose

	# for i in range(len(usefulData)):
	# 	count = count + 1
	# 	usefulData[i][2] = usefulData[i][2].replace("\n", "")			# here I remove the line break after each keystroke value
	# 	usefulData[i][2] = usefulData[i][2].replace(" ", "[space]")		# and also change the space value to be represented as "[space]" instead of " "
		
	# if printInfo:
	# 	print ""
	# 	print "[+] RETRIEVED USEFUL DATA from the input file."
	# 	print "    -> number of valid keystrokes: " + str(count)
	# 	print ""

	# return usefulData

