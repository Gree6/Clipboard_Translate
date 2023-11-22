# Clipboard_Translate
Features built into the google_trans_new Python package for batch file translation, clipboard translate.

![image](https://github.com/Gree6/Clipboard_Translate/assets/94130408/29d64f47-89af-4e67-a63f-9259238fa880)


## Features
- Auto-Grab whats in your clipboard (update automatically) or txt file (input.txt)
- Using google_trans_new to access Google Translate
- Translated txt appear in output text block

### Package Bug
Bug in google_trans_new.py line 151
change  response = (decoded_line + ']') to change  response = (decoded_line)

### Requirements
six
google_trans_new 
requests
