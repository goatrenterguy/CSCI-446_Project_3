from FileParser import FileParser
from ExactInference import ExactInference
from ApproximateInference import ApproximateInference


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
        #print("Select a network:\nA: Alarm\nC: Child\nH: Hailfinder\nI: Insurance\nW: Win95pts")
        #selection = input().upper()
        #try:
        #    filePath = "Networks/" + self.selectionKey[selection].lower() + ".bif"
        #    BNet = self.fileParser.readFile(filePath)
        #    print("File: " + filePath + " opened")
        #    factor = ExactInference().eliminationAsk(X='HYPOVOLEMIA', e={"HRBP": "HIGH", "CO": "LOW", "BP": "HIGH"}, BNet=BNet)

        # print('------------ ALARM NETWORK ------------')
        # BNet = self.fileParser.readFile('Networks/alarm.bif')
        # x = ['HYPOVOLEMIA', 'LVFAILURE', 'ERRLOWOUTPUT']
        # e = {"HRBP": "HIGH", "CO": "LOW", "BP": "HIGH"}
        # alarm_le = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=400)
        # print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
        # print(str(alarm_le))
        # print()
        # for X in x:
        #     print('Exact probabilities for ' + X + ', given known evidence ' + str(e))
        #     factor = ExactInference().eliminationAsk(X, e, BNet)
        #     print(factor.cpt)
        #     print()
        # x = ['HYPOVOLEMIA', 'LVFAILURE', 'ERRLOWOUTPUT']
        # e = {"HRBP": "HIGH", "CO": "LOW", "BP": "HIGH", 'HRSAT': 'LOW', 'HREKG': 'LOW'}
        # alarm_me = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=400)
        # print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
        # print(str(alarm_me))
        # print()
        # for X in x:
        #     print('Exact probabilities for ' + X + ', given known evidence ' + str(e))
        #     factor = ExactInference().eliminationAsk(X, e, BNet)
        #     print(factor.cpt)
        #     print()

        print('------------ CHILD NETWORK ------------')
        BNet = self.fileParser.readFile('Networks/child.bif')
        x = ['Disease']
        e = {'LowerBodyO2': '<5', 'RUQO2': '>=12', 'CO2Report': '>=7.5', 'XrayReport': 'Asy/Patchy'}
        child_le = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=1000)
        print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
        print(str(child_le))
        print()
        for X in x:
            print('Exact probabilities for ' + X + ', given known evidence ' + str(e))
            factor = ExactInference().eliminationAsk(X, e, BNet)
            print(factor.cpt)
            print()
        x = ['Disease']
        e = {'LowerBodyO2': '<5', 'RUQO2': '>=12', 'CO2Report': '>=7.5', 'XrayReport': 'Asy/Patchy',
             'GruntingReport': 'yes', 'LVHReport': 'yes', 'Age': '11-30_days'}
        child_me = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=1000)
        print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
        print(str(child_me))
        print()
        for X in x:
            print('Exact probabilities for ' + X + ', given known evidence ' + str(e))
            factor = ExactInference().eliminationAsk(X, e, BNet)
            print(factor.cpt)
            print()

        print('------------ HAILFINDER NETWORK ------------')
        BNet = self.fileParser.readFile('Networks/hailfinder.bif')
        x = ['SatContMoist', 'LLIW']
        e = {'RSFest': 'XNIL', 'N32StarFest': 'XNIL', 'MountainFest': 'XNIL', 'AreaMoDryAir': 'VeryWet'}
        hailfinder_le = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=1000)
        print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
        print(str(hailfinder_le))
        print()
        for X in x:
            print('Exact probabilities for ' + X + ', given known evidence ' + str(e))
            factor = ExactInference().eliminationAsk(X, e, BNet)
            print(factor.cpt)
            print()
        x = ['SatContMoist', 'LLIW']
        e = {'RSFest': 'XNIL', 'N32StarFest': 'XNIL', 'MountainFest': 'XNIL', 'AreaMoDryAir': 'VeryWet',
             'CombVerMo': 'Down', 'AreaMeso_ALS': 'Down', 'CurPropConv': 'Strong'}
        hailfinder_me = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=1000)
        print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
        print(str(hailfinder_me))
        print()
        for X in x:
            print('Exact probabilities for ' + X + ', given known evidence ' + str(e))
            factor = ExactInference().eliminationAsk(X, e, BNet)
            print(factor.cpt)
            print()

        print('------------ INSURANCE NETWORK ------------')
        BNet = self.fileParser.readFile('Networks/insurance.bif')
        x = ['MedCost', 'ILiCost', 'PropCost']
        e = {'Age': 'Adolescent', 'GoodStudent': 'False', 'SeniorTrain': 'False', 'DrivQuality': 'Poor'}
        insurance_le = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=1000)
        print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
        print(str(insurance_le))
        print()
        for X in x:
            print('Exact probabilities for ' + X + ', given known evidence ' + str(e))
            factor = ExactInference().eliminationAsk(X, e, BNet)
            print(factor.cpt)
            print()
        x = ['MedCost', 'ILiCost', 'PropCost']
        e = {'Age': 'Adolescent', 'GoodStudent': 'False', 'SeniorTrain': 'False', 'DrivQuality': 'Poor',
             'MakeModel': 'Luxury', 'CarValue': 'FiftyThou', 'DrivHistory': 'Zero'}
        insurance_me = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=1000)
        print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
        print(str(insurance_me))
        print()
        for X in x:
            print('Exact probabilities for ' + X + ', given known evidence ' + str(e))
            factor = ExactInference().eliminationAsk(X, e, BNet)
            print(factor.cpt)
            print()

        print('------------ Win95 NETWORK ------------')
        BNet = self.fileParser.readFile('Networks/win95pts.bif')
        x = ['Problem1', 'Problem2', 'Problem3', 'Problem4', 'Problem5', 'Problem6']
        e = {'Problem1': 'No_Output'}
        win95_1 = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=1000)
        print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
        print(str(win95_1))
        print()
        for X in x:
            print('Exact probabilities for ' + X + ', given known evidence ' + str(e))
            factor = ExactInference().eliminationAsk(X, e, BNet)
            print(factor.cpt)
            print()
        x = ['Problem1', 'Problem2', 'Problem3', 'Problem4', 'Problem5', 'Problem6']
        e = {'Problem2': 'Too_Long'}
        win95_2 = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=1000)
        print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
        print(str(win95_2))
        print()
        for X in x:
            print('Exact probabilities for ' + X + ', given known evidence ' + str(e))
            factor = ExactInference().eliminationAsk(X, e, BNet)
            print(factor.cpt)
            print()
        x = ['Problem1', 'Problem2', 'Problem3', 'Problem4', 'Problem5', 'Problem6']
        e = {'Problem3': 'No'}
        win95_3 = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=1000)
        print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
        print(str(win95_3))
        print()
        for X in x:
            print('Exact probabilities for ' + X + ', given known evidence ' + str(e))
            factor = ExactInference().eliminationAsk(X, e, BNet)
            print(factor.cpt)
            print()
        x = ['Problem1', 'Problem2', 'Problem3', 'Problem4', 'Problem5', 'Problem6']
        e = {'Problem4': 'No'}
        win95_4 = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=1000)
        print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
        print(str(win95_4))
        print()
        for X in x:
            print('Exact probabilities for ' + X + ', given known evidence ' + str(e))
            factor = ExactInference().eliminationAsk(X, e, BNet)
            print(factor.cpt)
            print()
        x = ['Problem1', 'Problem2', 'Problem3', 'Problem4', 'Problem5', 'Problem6']
        e = {'Problem5': 'No'}
        win95_5 = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=1000)
        print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
        print(str(win95_5))
        print()
        for X in x:
            print('Exact probabilities for ' + X + ', given known evidence ' + str(e))
            factor = ExactInference().eliminationAsk(X, e, BNet)
            print(factor.cpt)
            print()
        x = ['Problem1', 'Problem2', 'Problem3', 'Problem4', 'Problem5', 'Problem6']
        e = {'Problem6': 'Yes'}
        win95_6 = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=1000)
        print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
        print(str(win95_6))
        print()
        for X in x:
            print('Exact probabilities for ' + X + ', given known evidence ' + str(e))
            factor = ExactInference().eliminationAsk(X, e, BNet)
            print(factor.cpt)
            print()


if __name__ == "__main__":
    Main().selectionPrompt()
    # bn = FileParser().readFile("Networks/dog-problem.bif")
    # factor = ExactInference().eliminationAsk(X='family-out', e={'hear-bark': 'true', 'light-on': 'true'}, BNet=bn)
    # BNet = FileParser().readFile("Networks/alarm.bif")
    # factor = ExactInference().eliminationAsk(X='HYPOVOLEMIA', e={'CO': 'LOW'}, BNet=BNet)
    # factor = ExactInference().eliminationAsk(X='ERRLOWOUTPUT', e={"HRBP": "HIGH", "CO": "LOW", "BP": "HIGH"}, BNet=BNet)
    # print(factor.variables)
    # print(factor.cpt)


