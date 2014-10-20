import os
import urllib
import urllib2
from sys import argv
import time

def text2voicefile(text, fichero): # Dado un texto, te lo guarda en audio en un fichero.
	texturl = urllib.quote_plus(text)   
	url = "http://translate.google.com/translate_tts?tl=en&q="
	command = "wget -q -U Mozilla -O " + fichero +  " \"" + url + texturl + "\""
	#print command
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

def findcharmax(cadena, longitudma, caracter): # busca el caracter mas a la derecha sin pasarse del longitudma
	cont = longitudma 
	if len(cadena) < longitudma:
                 return -1
	for i in reversed(cadena[0:longitudma + 1]):
		if i == caracter:
			return cont
		cont -= 1
        return -1


def dividesentence(parrafo, maxlength, frases):
	if len(parrafo) < maxlength:
		frases.append(parrafo) # Si la frase cabe, la pone 
		return frases
	else:
		punto = findcharmax(parrafo, maxlength, ".")
	        if punto > -1:
			frases.append(parrafo[0:punto+1]) # Anade la primera mitad
			return dividesentence(parrafo[punto + 1:len(parrafo)-1], maxlength, frases) # Resuelve el problema para la segunda mitad 
		else:
			coma = findcharmax(parrafo, maxlength, ",")
	        	if coma > -1:
				frases.append(parrafo[0:coma+1]) # Anade la primera mitad
                        	return dividesentence(parrafo[coma + 1:len(parrafo)-1], maxlength, frases) # Resuelve el problema para la segunda mitad
			else:
				espacio = findcharmax(parrafo, maxlength, " ")
		        	if espacio > -1:
					frases.append(parrafo[0:espacio])
					return dividesentence(parrafo[espacio + 1:len(parrafo)-1], maxlength, frases) #llamada recursiva espacio
				else:
					frases.append(parrafo[0:maxlength])
					return dividesentence(parrafo[maxlength + 1:len(parrafo)-1], maxlength, frases) #llamada recursiva maxlength

script, fichero = argv
text = open(fichero).read()
parrafos = text.split('*')
cont = 0

for i in reversed(parrafos):
	frases = dividesentence(i, 100, [])
	with open("Audio" + str(cont) + ".mp3", 'wb') as file:
		for j in frases:
			response = get_google_voice(j)
			file.write(response.read())
	file.close()
	cont += 1
