import os
from core.student import Student
from core.problem import Problem

class Submission:
    '''
    Submission class
    Represents a submission of a student
    (e.g. Lab1 Submission of Student A)

    '''
    def __init__(self, directory:str, student:Student):
        '''
        Create submission object from submission directory.
        directory: submission directory (with codes in it)
        student: Student instance
        '''
        directory = os.path.abspath(directory)
        if not os.path.isdir(directory):
            if os.path.isfile(directory):
                raise FileNotFoundError(f"{directory} is not a directory")
            else:
                os.makedirs(directory)
                print(f'warning: Directory {directory} doesn\'t exist, creating one')

        self.directory = directory
        self.student = student

        # List of Problem instance, which is run in parallel.
        self.problems = []


    def add_problem(self, problem:Problem):
        if not isinstance(problem, Problem):
            raise TypeError("add_problem: Given arg should be Problem instance")
        problem.set_submission(self)
        self.problems.append(problem)
    
