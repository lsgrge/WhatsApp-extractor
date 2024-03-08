# WhatsApp-extractor

A small script that convert a complete WhatsApp conversation into a stylized html file in conversation format.

## Usage 

1. Export from WhatsApp a conversation with attachments.
2. unzip the archive
3. sanityze the _chat.txt file by removing the errors entrances like '[U+200E]' in the file. You can do this with the option 'Change all occurrences' in VS Code.
4. Lunch the script :

` python script.py input.txt output.html chemin_pieces_jointes author `

Author is your name in the conversation like 'LOUIS'. 

## Create a PDF of the conversation

You will be provide with a formated html file. You can open it in your web browser and print it as a PDF. Be sure to select the option 'Background Graphics' before printing. 

Here you have a Whatsapp formatted PDF of your conversation with pictures embeded !

