# keystroke-analysis
caseyscarborough made keylogger for mac: https://github.com/caseyscarborough/keylogger <br>
adam harvey added nano second timestamps to it: https://github.com/adamhrv/keylogger<br>
before capturing keystrokes to be used with my script, I recommend doing this:<br>
open the keylogger.c file of keylogger<br>
go to line 168<br>
replace:<br>
case 49:  return " ";<br>
with<br>
case 49:  return "[space]";<br><br>

my script builds upon the keylogger's output file in csv format. 

1) 	<b>change the parameters in the settings file.</b> <br>
2)	<b>run script like this:</b> <br>
 			$ python keystroke_analysis.py keystrokes.csv <br>
	<b>in order to export to a csv file run like this:</b> <br>
			$ python keystroke_analysis.py keystrokes.csv outFile.csv <br>


![alt tag](https://raw.github.com/leoneckert/keystroke-analysis/master/raw_fingerprint.png)

<br>
[+] To do:<br>
- At the moment I am experimenting with different ways of visualising the output table through processing. The aim is a visual representation of ones keystroke fingerprint that can be compared with others.<br>
- ultimately it would be nice to have a small web application i which a user types while the fingerprint is generated live.<br>
- ... 