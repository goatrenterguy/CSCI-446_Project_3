from FileParser import FileParser as FP
from ExactInference import ExactInference
import ApproximateInference


class Main:
    def __init__(self):
        self.fileParser = FP()
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
        print(ExactInference().eliminationAsk(X='HYPOVOLEMIA', e={"HRBP": "HIGH", "CO": "LOW", "BP": "HIGH"}, BNet=BNet))

        # except:
        #     print("Invalid selection please try again\n+---------------------------+\n")
        #     self.selectionPrompt()


if __name__ == "__main__":
    main = Main()
    main.selectionPrompt()
