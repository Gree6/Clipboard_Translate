# Clipboard_Translate
Grab from clipboard/file, translate and display and save it

## Flow
- Auto-Grab whats in your clipboard (update automatically) or txt file
- Google Translate
- Save it to a txt file and make it visible in gui
- Repeats with file and clipboard changes

### Bugs
Bug in google_trans_new.py line 151
change  response = (decoded_line + ']') to change  response = (decoded_line)
