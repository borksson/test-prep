import TestPrep_classes
import json

with open("appData.json", "r") as appData:
    app = TestPrep_classes.App(json.load(appData))

# Operations on app
#app.parse_dir_notes()
#app.set_to_quizlet()


with open("appData.json", "w") as appData:
    appData.write(app.to_string())
