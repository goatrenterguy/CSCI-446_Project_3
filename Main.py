from FileParser import FileParser
from ExactInference import ExactInference
from ApproximateInference import ApproximateInference

class Main:
    def experiment(self):
        print('------------ ALARM NETWORK ------------')
        BNet = FileParser().readFile('Networks/alarm.bif')
        x = ['HYPOVOLEMIA', 'LVFAILURE', 'ERRLOWOUTPUT']

        # No evidence
        e = {}
        alarm_ne = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=400, demo_flag=False)
        print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
        print(str(alarm_ne))
        print()
        for X in x:
            print('Exact probabilities for ' + X + ', given known evidence ' + str(e))
            factor = ExactInference().eliminationAsk(X, e, BNet)
            print(factor.cpt)
            print()

        # Little evidence
        e = {"HRBP": "HIGH", "CO": "LOW", "BP": "HIGH"}
        alarm_le = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=400, demo_flag=False)
        print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
        print(str(alarm_le))
        print()
        for X in x:
            print('Exact probabilities for ' + X + ', given known evidence ' + str(e))
            factor = ExactInference().eliminationAsk(X, e, BNet)
            print(factor.cpt)
            print()

        # Moderate evidence
        e = {"HRBP": "HIGH", "CO": "LOW", "BP": "HIGH", 'HRSAT': 'LOW', 'HREKG': 'LOW'}
        alarm_me = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=400, demo_flag=False)
        print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
        print(str(alarm_me))
        print()
        for X in x:
            print('Exact probabilities for ' + X + ', given known evidence ' + str(e))
            factor = ExactInference().eliminationAsk(X, e, BNet)
            print(factor.cpt)
            print()

        print('------------ CHILD NETWORK ------------')
        BNet = FileParser().readFile('Networks/child.bif')
        x = ['Disease']
        # No evidence
        e = {}
        child_ne = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=1000, demo_flag=False)
        print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
        print(str(child_ne))
        print()
        for X in x:
            print('Exact probabilities for ' + X + ', given known evidence ' + str(e))
            factor = ExactInference().eliminationAsk(X, e, BNet)
            print(factor.cpt)
            print()

        # Little evidence
        e = {'LowerBodyO2': '<5', 'RUQO2': '>=12', 'CO2Report': '>=7.5', 'XrayReport': 'Asy/Patchy'}
        child_le = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=1000, demo_flag=False)
        print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
        print(str(child_le))
        print()
        for X in x:
            print('Exact probabilities for ' + X + ', given known evidence ' + str(e))
            factor = ExactInference().eliminationAsk(X, e, BNet)
            print(factor.cpt)
            print()

        # Moderate evidence
        e = {'LowerBodyO2': '<5', 'RUQO2': '>=12', 'CO2Report': '>=7.5', 'XrayReport': 'Asy/Patchy',
             'GruntingReport': 'yes', 'LVHReport': 'yes', 'Age': '11-30_days'}
        child_me = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=1000, demo_flag=False)
        print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
        print(str(child_me))

        print('------------ CHILD NETWORK ------------')
        BNet = FileParser().readFile('Networks/child.bif')
        x = ['Disease']
        e = {'LowerBodyO2': '<5', 'RUQO2': '>=12', 'CO2Report': '>=7.5', 'XrayReport': 'Asy/Patchy'}
        child_le = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=1000, demo_flag=False)
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
        child_me = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=1000, demo_flag=False)
        print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
        print(str(child_me))
        print()
        for X in x:
            print('Exact probabilities for ' + X + ', given known evidence ' + str(e))
            factor = ExactInference().eliminationAsk(X, e, BNet)
            print(factor.cpt)
            print()

            print('------------ HAILFINDER NETWORK ------------')
            BNet = FileParser().readFile('Networks/hailfinder.bif')
            x = ['SatContMoist', 'LLIW']

            # No evidence
            e = {}
            hailfinder_ne = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=1000, demo_flag=False)
            print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
            print(str(hailfinder_ne))
            print()
            for X in x:
                print('Exact probabilities for ' + X + ', given known evidence ' + str(e))
                factor = ExactInference().eliminationAsk(X, e, BNet)
                print(factor.cpt)
                print()

            # Little evidence
            e = {'RSFest': 'XNIL', 'N32StarFest': 'XNIL', 'MountainFest': 'XNIL', 'AreaMoDryAir': 'VeryWet'}
            hailfinder_le = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=1000, demo_flag=False)
            print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
            print(str(hailfinder_le))
            print()
            for X in x:
                print('Exact probabilities for ' + X + ', given known evidence ' + str(e))
                factor = ExactInference().eliminationAsk(X, e, BNet)
                print(factor.cpt)
                print()

            # Moderate evidence
            e = {'RSFest': 'XNIL', 'N32StarFest': 'XNIL', 'MountainFest': 'XNIL', 'AreaMoDryAir': 'VeryWet',
                 'CombVerMo': 'Down', 'AreaMeso_ALS': 'Down', 'CurPropConv': 'Strong'}
            hailfinder_me = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=1000, demo_flag=False)
            print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
            print(str(hailfinder_me))

            print('------------ HAILFINDER NETWORK ------------')
            BNet = FileParser().readFile('Networks/hailfinder.bif')
            x = ['SatContMoist', 'LLIW']
            e = {'RSFest': 'XNIL', 'N32StarFest': 'XNIL', 'MountainFest': 'XNIL', 'AreaMoDryAir': 'VeryWet'}
            hailfinder_le = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=1000, demo_flag=False)
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
            hailfinder_me = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=1000, demo_flag=False)
            print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
            print(str(hailfinder_me))
            print()

            for X in x:
                print('Exact probabilities for ' + X + ', given known evidence ' + str(e))
                factor = ExactInference().eliminationAsk(X, e, BNet)
                print(factor.cpt)
                print()

                print('------------ INSURANCE NETWORK ------------')
                BNet = FileParser().readFile('Networks/insurance.bif')
                x = ['MedCost', 'ILiCost', 'PropCost']

                # No evidence
                e = {}
                insurance_ne = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=1000, demo_flag=False)
                print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
                print(str(insurance_ne))
                print()
                for X in x:
                    print('Exact probabilities for ' + X + ', given known evidence ' + str(e))
                    factor = ExactInference().eliminationAsk(X, e, BNet)
                    print(factor.cpt)
                    print()

                # Little evidence
                e = {'Age': 'Adolescent', 'GoodStudent': 'False', 'SeniorTrain': 'False', 'DrivQuality': 'Poor'}
                insurance_le = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=1000, demo_flag=False)
                print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
                print(str(insurance_le))
                print()
                for X in x:
                    print('Exact probabilities for ' + X + ', given known evidence ' + str(e))
                    factor = ExactInference().eliminationAsk(X, e, BNet)
                    print(factor.cpt)
                    print()

                # Moderate evidence
                e = {'Age': 'Adolescent', 'GoodStudent': 'False', 'SeniorTrain': 'False', 'DrivQuality': 'Poor',
                     'MakeModel': 'Luxury', 'CarValue': 'FiftyThou', 'DrivHistory': 'Zero'}
                insurance_me = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=1000, demo_flag=False)
                print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
                print(str(insurance_me))

            print('------------ INSURANCE NETWORK ------------')
            BNet = FileParser().readFile('Networks/insurance.bif')
            x = ['MedCost', 'ILiCost', 'PropCost']
            e = {'Age': 'Adolescent', 'GoodStudent': 'False', 'SeniorTrain': 'False', 'DrivQuality': 'Poor'}
            insurance_le = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=1000, demo_flag=False)
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
            insurance_me = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=1000, demo_flag=False)
            print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
            print(str(insurance_me))
            print()
            for X in x:
                print('Exact probabilities for ' + X + ', given known evidence ' + str(e))
                factor = ExactInference().eliminationAsk(X, e, BNet)
                print(factor.cpt)
                print()

                print('------------ Win95 NETWORK ------------')
                BNet = FileParser().readFile('Networks/win95pts.bif')
                x = ['Problem1', 'Problem2', 'Problem3', 'Problem4', 'Problem5', 'Problem6']

                # No evidence
                e = {}
                for x in X:
                    win95_ne = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=1000, demo_flag=False)
                    print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
                    print(str(win95_ne))
                    print()
                    print('Exact probabilities for ' + X + ', given known evidence ' + str(e))
                    factor = ExactInference().eliminationAsk(X, e, BNet)
                    print(factor.cpt)
                    print()

                e = {'Problem1': 'No_Output'}

                win95_1 = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=1000, demo_flag=False)
                print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
                print(str(win95_1))
                print()
                for X in x:
                    print('Exact probabilities for ' + X + ', given known evidence ' + str(e))
                    factor = ExactInference().eliminationAsk(X, e, BNet)
                    print(factor.cpt)
                    print()
                e = {'Problem2': 'Too_Long'}
                win95_2 = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=1000, demo_flag=False)
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
                win95_3 = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=1000, demo_flag=False)
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
                win95_4 = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=1000, demo_flag=False)
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
                win95_5 = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=1000, demo_flag=False)
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
                win95_6 = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=1000, demo_flag=False)
                print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
                print(str(win95_6))
                print()
                for X in x:
                    print('Exact probabilities for ' + X + ', given known evidence ' + str(e))
                    factor = ExactInference().eliminationAsk(X, e, BNet)
                    print(factor.cpt)
                    print()

    def demo(self):
        print('------------ ALARM NETWORK ------------')
        BNet = FileParser().readFile('Networks/alarm.bif')
        x = ['HYPOVOLEMIA', 'LVFAILURE', 'ERRLOWOUTPUT']

        # No evidence
        e = {}
        alarm_ne = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=400, demo_flag=True)
        print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
        print(str(alarm_ne))
        print()
        for X in x:
            print('Exact probabilities for ' + X + ', given known evidence ' + str(e))
            factor = ExactInference().eliminationAsk(X, e, BNet)
            print(factor.cpt)
            print()

        # Little evidence
        e = {"HRBP": "HIGH", "CO": "LOW", "BP": "HIGH"}
        alarm_le = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=400, demo_flag=True)
        print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
        print(str(alarm_le))
        print()
        for X in x:
            print('Exact probabilities for ' + X + ', given known evidence ' + str(e))
            factor = ExactInference().eliminationAsk(X, e, BNet)
            print(factor.cpt)
            print()

        # Moderate evidence
        e = {"HRBP": "HIGH", "CO": "LOW", "BP": "HIGH", 'HRSAT': 'LOW', 'HREKG': 'LOW'}
        alarm_me = ApproximateInference().gibbsAsk(X=x, e=e, bnet=BNet, n=400, demo_flag=True)
        print('Approximate probabilities for ' + str(x) + ', given known evidence: ' + str(e))
        print(str(alarm_me))
        print()
        for X in x:
            print('Exact probabilities for ' + X + ', given known evidence ' + str(e))
            factor = ExactInference().eliminationAsk(X, e, BNet)
            print(factor.cpt)
            print()



if __name__ == "__main__":
    print('Demo or experiment (d/e) ->  ')
    x = input()
    if x == 'e':
        Main().experiment()
    else:
        Main().demo()