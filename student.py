class Student:
    '''
    Student class, who submitted his/her code for evaluation
    '''
    def __init__(self, name):
        self.name = name
        self.student_no = ''
        self.directorypath = ''
        self.submissions = [] # list containing ProbResult

class StudentResult:
    pass