from FileParser import FileParser
from ExactInference import ExactInference
from ApproximateInference import ApproximateInference

if __name__ == "__main__":
    print('------------ DOG-PROBLEM NETWORK ------------')
    BNet = FileParser().readFile('Networks/dog-problem.bif')
    demo = ExactInference().eliminationAsk(X='family-out', e={'light-on': 'true', 'hear-bark': 'true'}, BNet=BNet, demo=True)
    print(demo.cpt)
