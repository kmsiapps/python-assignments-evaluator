class Problem:
    '''
    Class for problem definition, such as name, points, etc.
    '''
    def __init__(self):
        self.name = ''
        self.tests = []
        self.points = 0

class ProbResult:
    '''
    Problem evaluation result class containing multiple test evaluation results
    '''
    def __init__(self):
        self.problem = None
