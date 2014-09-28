### By Ariana Giorgi
### 09/26/14
### Computational Journalism, TF-IDF Assignment for State-of-Union Addresses

import csv
import string
import math
import operator

csv.field_size_limit(1000000000) #reset limit to number of lines

#-----Open data file-----
text = {} #initializing a text dictionary

with open('state-of-the-union.csv', 'rb') as csvfile:
	"""Read CSV file"""
	reader = csv.reader(csvfile)

	speech = ""
	words = []

	for row in reader:
		for i in range(len(row)):
			if i == 1: #the speech part of the row
				speech = row[1]
				
				#-----Tokenize text-----
				speech = speech.lower() #set to lowercase
				for c in string.punctuation: #remove punctuation
					speech = speech.replace(c,"")
				speech = string.replace(speech, "\n", " ") #replace new line with just space
				words = string.split(speech) #create list of words from speech split by spaces
			text[row[0]] = words
			#created dictionary where keys = year and values = tokenized speech
	
#-----TF Vector-----
termfreq = {}
word = ""

for k in text:
	word_lst = {}
	for v in range(len(text[k])): #loop through words in each speech
		word = text[k][v]
		if (word in word_lst):
			word_lst[word] += 1 #increase word count
		else:
			word_lst[word] = 1 #add word to list
	termfreq[k] = word_lst #replace the values in the dictionary with word count

#print termfreq['1960']
#print termfreq['1960']['the']

#-----Word Document Count-----
wordcount = {} #initialize word count dictionary
numDocs = 0 #initialize number of documents

for k in termfreq:
	numDocs += 1 #simultaneously count the numbers of documents
	for v in termfreq[k]:
		if (v in wordcount):
			wordcount[v] += 1 #if word appears in document, increase document count
		else:
			wordcount[v] = 1

#-----IDF-----
IDFterms = {}

for k in wordcount:
	IDFterms[k] = math.log(numDocs/wordcount[k]) #apply IDF formula

#-----TF-IDF-----
tfidf = {} #will hold document id and tfidf vector

for k in termfreq:
	temp_lst = {}
	for v in termfreq[k]:
		x = IDFterms[v] * termfreq[k][v] #value for each word is TF * IDF weights
		temp_lst[v] = x
	tfidf[k] = temp_lst

#-----Normalize-----
for k in tfidf:
	lengthsq = 0
	for v in tfidf[k]:
		lengthsq = lengthsq + (tfidf[k][v] ** 2) #square all the values and add them together
	length = math.sqrt(lengthsq) #take squareroot to find length
	for v in tfidf[k]:
		tfidf[k][v] = tfidf[k][v]/length #divide each value by the length to normalize

#-----1960 speech-----
sorted1960 = []
sorted1960 = sorted(tfidf['1960'].items(), key=operator.itemgetter(1), reverse=True) #sorts the tfidf vector of 1960 by weight

with open('1960output.txt', 'w') as output:
	for i in range(0,20):
		output.write(str(i+1) + ". " + str(sorted1960[i])+"\n") #print top 20 terms to file

#-----Decades of Speeches-----
decades = {}
with open('Decades_output.txt', 'w') as f: #create file for top terms of each decade
	for i in range(0,12):
		terms = {}
		start = 1900 + (10 * i) #the decades ie 1900, 1910
		for j in range(0,10):
			year = str(start + j) #the individual years within the decade ie 1901
			if year in tfidf:
				for v in tfidf[year]: #v is word in list of terms
					if v in terms:
						terms[v] = terms[v] + tfidf[year][v] #add weights of that decade together for that term
					else:
						terms[v] = tfidf[year][v]
		decades[str(start)] = sorted(terms.items(), key=operator.itemgetter(1), reverse=True) #sort the list of terms
		f.write(str(start)+"s:\n") #write decade
		for k in range(0,20):
			f.write(str(k+1) + ". " + str(decades[str(start)][k]) + "\n") #write top 20 terms for each decade to file


