from FileParser import FileParser
from ExactInference import ExactInference
import ApproximateInference


class Main:
    def __init__(self):
        self.fileParser = FileParser()
        self.selectionKey = {
            "A": "Alarm",
            "C": "Child",
            "H": "Hailfinder",
            "I": "Insurance",
            "W": "Win95pts"
        }

    def selectionPrompt(self):
        print("Select a network:\nA: Alarm\nC: Child\nH: Hailfinder\nI: Insurance\nW: Win95pts")
        selection = input().upper()
        # try:
        filePath = "Networks/" + self.selectionKey[selection].lower() + ".bif"
        BNet = self.fileParser.readFile(filePath)
        print("File: " + filePath + " opened")
        factor = ExactInference().eliminationAsk(X='HYPOVOLEMIA', e={"HRBP": "HIGH", "CO": "LOW", "BP": "HIGH"}, BNet=BNet)
        print(factor.variables)
        print(factor.cpt)

        # except:
        #     print("Invalid selection please try again\n+---------------------------+\n")
        #     self.selectionPrompt()


if __name__ == "__main__":
    # main = Main()
    # main.selectionPrompt()
    # bn = FileParser().readFile("Networks/dog-problem.bif")
    # factor = ExactInference().eliminationAsk(X='family-out', e={'light-on': 'true', 'hear-bark': 'true'}, BNet=bn)
    BNet = FileParser().readFile("Networks/alarm.bif")
    factor = ExactInference().eliminationAsk(X='HYPOVOLEMIA', e={'CO': 'LOW'}, BNet=BNet)
    # factor = ExactInference().eliminationAsk(X='ERRLOWOUTPUT', e={"HRBP": "HIGH", "CO": "LOW", "BP": "HIGH"}, BNet=BNet)
    print(factor.variables)
    print(factor.cpt)


