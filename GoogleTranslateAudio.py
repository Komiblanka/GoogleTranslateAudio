# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4:
import os
import urllib
import urllib2
from sys import argv
import time


def text2voicefile(text, text_file): # Dado un texto, te lo guarda en audio en un text_file.
	text_url = urllib.quote_plus(text)   
	url = "http://translate.google.com/translate_tts?tl=en&q="
	command = "wget -q -U Mozilla -O " + text_file +  " \"" + url + text_url + "\""
	os.system(command)
    
def get_google_voice(phrase):
	language='en' #Setting language.
	url = "http://translate.google.com/translate_tts" #Google translate url for getting sound.
	user_agent="Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5."
	file_name="temp.mp3" #Temp file for saving our voiced phrase.
     
	params = urllib.urlencode({'q':phrase, 'tl':language}) #query parameters.
	request = urllib2.Request(url, params) #http request.
	request.add_header('User-Agent', user_agent) #adding agent as header.
	response = urllib2.urlopen(request)
	return response

def findcharmax(text_string, max_string_length, character): # busca el character mas a la derecha sin pasarse del max_string_length
    counter = max_string_length 
    if len(text_string) < max_string_length:
        return -1
    for i in reversed(text_string[0:max_string_length + 1]):
        if i == character:
            return counter
        counter -= 1
    return -1

def divide_sentence(paragraph, maxlength, phrases):
    if len(paragraph) < maxlength:
        phrases.append(paragraph) # Si la frase cabe, la pone 
        return phrases
    characters = ".", ",", " "

    for character in characters: #go through all characters
        position = findcharmax(paragraph, maxlength, character)
        if position > -1:
            phrases.append(paragraph[0:position])
            return divide_sentence(paragraph[position + 1:len(paragraph)-1], maxlength, phrases) #llamada recursiva position 
    
    phrases.append(paragraph[0:maxlength])
    return divide_sentence(paragraph[maxlength + 1:len(paragraph)-1], maxlength, phrases) #llamada recursiva maxlength

script, text_file = argv
text = open(text_file).read()
paragraphs = text.split('*')
counter = 0

for i in paragraphs:
	phrases = divide_sentence(i, 100, [])
	with open("Audio" + str(counter) + ".mp3", 'wb') as file:
		for j in phrases:
			response = get_google_voice(j)
			file.write(response.read())
	file.close()
	counter += 1
