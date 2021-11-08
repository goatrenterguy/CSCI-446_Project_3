from FileParser import FileParser as FP
from ExactInference import ExactInference
from ApproximateInference import ApproximateInference


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
        #print("Select a network:\nA: Alarm\nC: Child\nH: Hailfinder\nI: Insurance\nW: Win95pts")
        #selection = input().upper()
        # try:
        #filePath = "Networks/" + self.selectionKey[selection].lower() + ".bif"
        #BNet = self.fileParser.readFile(filePath)
        #print("File: " + filePath + " opened")
        # factor = ExactInference().eliminationAsk(X='HYPOVOLEMIA', e={"HRBP": "HIGH", "CO": "LOW", "BP": "HIGH"}, BNet=BNet)
        BNet = self.fileParser.readFile('Networks/alarm.bif')
        alarm_le = ApproximateInference().gibbsAsk(X=['HYPOVOLEMIA', 'LVFAILURE', 'ERRLOWOUTPUT'],
                                                   e={"HRBP": "HIGH", "CO": "LOW", "BP": "HIGH"}, bnet=BNet, n=1000)
        print('Alarm little evidence: ' + str(alarm_le))
        alarm_me = ApproximateInference().gibbsAsk(X=['HYPOVOLEMIA', 'LVFAILURE', 'ERRLOWOUTPUT'],
                                                   e={"HRBP": "HIGH", "CO": "LOW", "BP": "HIGH", 'HRSAT': 'LOW',
                                                      'HREKG': 'LOW'}, bnet=BNet, n=1000)

        print('Alarm moderate evidence: ' + str(alarm_me))

        BNet = self.fileParser.readFile('Networks/child.bif')
        child = ApproximateInference().gibbsAsk(X=['Disease'], e={'LowerBodyO2': '"<5"', 'RUQO2': '">=12"', 'CO2Report': '">=7.5"', 'XrayReport': 'Asy/Patchy'}, bnet=BNet, n=1000)
        print('Child little evidence: ' + child)
        #print(factor.variables)
        #print(factor.cpt)

        # except:
        #     print("Invalid selection please try again\n+---------------------------+\n")
        #     self.selectionPrompt()


if __name__ == "__main__":
    main = Main()
    main.selectionPrompt()
