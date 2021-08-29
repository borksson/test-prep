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
from os import listdir, path, chdir, getcwd

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

SAVE_DATA = "/home/borkson/Code/Python/TestPrep/groupNotes.json"
builder = Gtk.Builder()
builder.add_from_file("FolderSelect.glade")

#Objects: card (term/definition, question/answer), cardSet (list of card objects, toJSON function)
# Handler (GTK application handler)
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

class Handler:
    def onDestroy(self, *args):
    	saveSets()
    	print('Sets saved.')
    	Gtk.main_quit()

    def buttonClick(self, folderSelection):
        print("Selected: ", folderSelection.get_filename(), 
        	builder.get_object("cardSetName").get_text())
        for file in listdir(folderSelection.get_filename()):
        	scanNote(folderSelection.get_filename()+'/'+file, findSet(builder.get_object("cardSetName").get_text()))
        	createQuizlet(folderSelection.get_filename(), findSet(builder.get_object("cardSetName").get_text()))
        printSets()
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
	#FIXME: Add scanDocx function
	print(noteFile, cardSet)
	with open(noteFile) as f:
		text = f.read()
		print(text)
	f.close()
	a = [card[:card.find("#E")].split("#D:") for card in text.split('#T:') if "#E" in card]
	for card in a:
		cardSet.addCard(card[0].strip(),card[1].strip())

def findSet(setName):
	for _set in sets:
		print(_set.setName, setName)
		if _set.setName == setName:
			return _set
	print("No set found. Creating set.")
	cardSet = CardSet(setName = setName) #FIXME: generate new random name that doesn't exist in sets
	sets.append(cardSet)
	return cardSet

def printSets():
	for _set in sets: _set.printSet()

def setsToJSON():
	export = []
	for _set in sets:
		export.append(_set.toJSON())
	return export

def saveSets():
	with open(SAVE_DATA, "w") as f:
		json.dump(setsToJSON(), f)
	f.close()

def createQuizlet(wd,cardSet):
	#FIXME: Scan for delilimters in terms and definitions (, & ;)
	with open(wd+'/'+cardSet.setName+"_quizlet.txt", "w") as f: 
		f.write(cardSet.toQuizlet())
	f.close()

#Open and load GroupNotes (groupNote.json will contain all saved sets)
sets = importSets(SAVE_DATA)
#print(findSet("Group Note Test"))

#Scan selected note documents
#Identify KeyNotes
#Create KeyNote objects, and add them to GroupNote

#scanNote("ClassName_2.3.20.txt", findSet("Group Note Test"))
printSets()

print('Sets loaded.')
#Save to JSON
#saveSets()

#Give option to create Quizlet document
#QUIZLET BULK TERM UPLOAD: Separate terms and definitions with a !comma!, tab, or dash.
#Separate rows with a !semicolon! or a new line. Each row of your document will become
#a distinct card.

#createQuizlet(findSet("UnnamedSet"))

#Optional TERM/DEFINITION could be a QUESTION/SINGLE_ANSWER or 
#QUESTION_MULTIPLE CHOICE/SINGLE_ANSWER

#Application init
builder.connect_signals(Handler())

window = builder.get_object("window1")
window.show_all()

Gtk.main()