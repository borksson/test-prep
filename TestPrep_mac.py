import json

# Card Set includes Term Card and Question Card

# Card (toJSON, toQuizlet, toString)
from typing import Any


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

    def to_dict(self):
        return [card.to_dict() for card in self.cardSet]

    def to_string(self):
        return json.dumps(self.to_dict())


# App (appData, cardSetObj)
class App(object):
    # Pass appData in as python dict
    def __init__(self, app_data):
        self.name = "Test Prep"
        self.appData = app_data
        self.cardSets = {key: CardSet(value) for key, value in self.appData['set'].items()}

    def to_dict(self):
        return {"name": self.name, "set": {key: value.to_dict() for key, value in self.cardSets.items()}}

    def to_string(self):
        return json.dumps(self.to_dict())


with open("appData.json", "r") as appData:
    app = App(json.load(appData))

# Operations on app
with open("appData.json", "w") as appData:
    appData.write(app.to_string())
