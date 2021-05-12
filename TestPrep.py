#How will this work? 1. Take marked notes in class. 2. The program will scan the notes and make a
#groupNote file. This file will contain a set with cards containing various terms and definitions
#3. In preperation for a test a Quizlet will be created, and it will be used to study the noted
#material.
#
#
# Q: What happens with different midterms? A: Seperate notes by midterms. You could use a folder
# hierarchy or a naming system. Or the group note could be created off of specific note files.
# So you would run the groupNote creator and select which files to scan to make a set. Maybe that
# can be implemented in the application. For now we will just scan all .txt documents in a 
# directory.

import json
from os import listdir, path

#Objects: card (term/definition, question/answer), cardSet (list of card objects, toJSON function)
class card(object):
	def __init__(self, term, definition):
		self.term = term
		self.definition = definition

	def toJSON(self):
		return {
	    	"term": self.term,
      		"definition": self.definition
		}

	def toQuizlet(self):
		return self.term+','+self.definition

	def printCard(self):
		print("Term: "+self.term+" Definition: "+self.definition)

class CardSet(object):
	"""docstring for set"""
	def __init__(self, setName, cards = []):
		self.setName = setName
		self.cards = cards
			
	def toJSON(self):
		export = []
		for card in self.cards:
			export.append(card.toJSON())
		return {
			"setName": self.setName,
			"cards": export
		}

	def toQuizlet(self):
		export = ""
		for card in self.cards:
			export+=card.toQuizlet()+";"
			#FIXME: ; on last card?
		return export

	def addCard(self, term, definition):
		#FIXME: Check to see if term exists in set
		self.cards.append(card(term=term, definition=definition))

	def printSet(self):
		print("Set name: "+self.setName+"\nCards: ")
		for card in self.cards:
			card.printCard()

#Functions: importSets (import groupNote.json files as active objects), scanNote(import noteFile and append to cardSet)

def importSets(JSONfile):
	with open(JSONfile) as f:
		try:
			setsRaw = json.load(f)
		except:
			setsRaw = []

	f.close()
	sets = []
	for _set in setsRaw:
		cards = []
		for _card in _set["cards"]:
			cards.append(card(_card["term"], _card["definition"]))
		sets.append(CardSet(setName = _set["setName"], cards = cards))
	return sets

def scanNote(noteFile, cardSet):
	if cardSet == None:
		print("Create set")
		cardSet = CardSet(setName = "UnnamedSet") #FIXME: generate new random name that doesn't exist in sets
		sets.append(cardSet)
	#FIXME: Add scanDocx function
	with open(noteFile) as f:
		text = f.read()
	f.close()
	a = [card[:card.find("#E")].split("#A:") for card in text.split('#T:') if "#E" in card]
	for card in a:
		cardSet.addCard(card[0].strip(),card[1].strip())

def findSet(setName):
	for _set in sets:
		if _set.setName == setName:
			return _set

def printSets():
	for _set in sets: _set.printSet()

def setsToJSON():
	export = []
	for _set in sets:
		export.append(_set.toJSON())
	return export

def saveSets():
	with open("groupNotes.json", "w") as f:
		json.dump(setsToJSON(), f)
	f.close()

def createQuizlet(cardSet):
	#FIXME: Scan for delilimters in terms and definitions (, & ;)
	with open(cardSet.setName+"_quizlet.txt", "w") as f: 
		f.write(cardSet.toQuizlet())
	f.close()

#Open and load GroupNotes (groupNote.json will contain all saved sets)
sets = importSets("groupNotes.json")

print(findSet("Group Note Test"))

#Scan selected note documents
#Identify KeyNotes
#Create KeyNote objects, and add them to GroupNote
scanNote("ClassName_2.3.20.txt", findSet("Group Note Test"))
printSets()

#Save to JSON
saveSets()

#Give option to create Quizlet document
#QUIZLET BULK TERM UPLOAD: Separate terms and definitions with a !comma!, tab, or dash.
#Separate rows with a !semicolon! or a new line. Each row of your document will become
#a distinct card.
createQuizlet(findSet("UnnamedSet"))

#Optional TERM/DEFINITION could be a QUESTION/SINGLE_ANSWER or 
#QUESTION_MULTIPLE CHOICE/SINGLE_ANSWER

