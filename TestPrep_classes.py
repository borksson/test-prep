import json
import os
import re


# Card Set includes Term Card and Question Card
# Card (toJSON, toQuizlet, toString)

class Card(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def to_dict(self):
        return {"key": self.key, "value": self.value}

    def to_string(self):
        return json.dumps(self.to_dict())


# Term Card (term, definition)
class TermCard(Card):
    def __init__(self, term, definition):
        Card.__init__(self, term, definition)


# Question Card (question, answer)
class QuestionCard(Card):
    def __init__(self, question, answer):
        Card.__init__(self, question, answer)


# Card Set (cardSet, toJSON, toQuizlet, toString)
class CardSet(object):
    def __init__(self, card_set):
        self.cardSet = [Card(card['key'], card['value']) for card in card_set]

    def add_card(self, card):
        # Check for duplicate cards/terms
        self.cardSet.append(card)

    def append(self, cards):
        for card in cards:
            self.add_card(card)

    def to_dict(self):
        return [card.to_dict() for card in self.cardSet]

    def to_string(self):
        return json.dumps(self.to_dict())


# App (appData, cardSetObj)
def parse_notes(file_name):
    card_set = []
    file_type = os.path.splitext(file_name)[1]
    if file_type == '.pdf':
        with open(file_name, 'rb') as file:
            data = os.popen("pdftotext %s -" % file_name).read()
            cards = [m[0] for m in re.finditer('(#T.*#D.*#E)|(#Q.*#A.*#E)', data)]
            for card in cards:
                card = card.split('#')
                card_set.append(Card(card[1][1:].strip(), card[2][1:].strip()))
    elif file_type == '.txt':
        with open(file_name) as file:
            data = file.read()
            cards = [m[0] for m in re.finditer('(#T.*#D.*#E)|(#Q.*#A.*#E)', data)]
            for card in cards:
                card = card.split('#')
                card_set.append(Card(card[1][1:].strip(), card[2][1:].strip()))
    elif file_type == '.md':
        with open(file_name) as file:
            data = file.read()
            cards = [m[0] for m in re.finditer('(>.*:.*\n)', data)]
            for card in cards:
                card = card.split(':')
                card_set.append(Card(card[0][1:].strip(), card[1].strip()))
    else:
        print(file_name+" is an invalid file type.")
    return card_set


class App(object):
    # Pass appData in as python dict
    def __init__(self, app_data):
        self.name = app_data['name']
        self.notes_dir = app_data['notes_dir']
        self.card_sets = {key: CardSet(value) for key, value in app_data['set'].items()}

    def to_dict(self):
        return {"name": self.name,"notes_dir":self.notes_dir, "set": {key: value.to_dict() for key, value in self.card_sets.items()}}

    def to_string(self):
        return json.dumps(self.to_dict())

    def add_card_set(self, key, card_set):
        self.card_sets[key] = card_set;

    def parse_dir_notes(self):
        key = os.path.basename(os.path.dirname(self.notes_dir))
        card_set = CardSet([])
        for file in os.listdir(self.notes_dir):
            card_set.append(parse_notes(self.notes_dir+'/'+file))
        self.add_card_set(key, card_set)

    def set_to_quizlet(self, key):
        export = ""
        for card in self.card_sets[key].to_dict():
            export += card['key'] + '#' + card['value'] + '$'
        with open(self.notes_dir+'/'+key+"_quizlet.txt", 'w') as file:
            file.write(export)

