import os
from core.student import Student
from core.problem import Problem
from core.task.task import Task

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

        # Tasks that are run beforehand. Executed sequentially.
        self.pretasks = []

        # List of Problem instance, which is run in parallel.
        self.problems = []

        # Tasks which are executed sequentially,
        # after all problems are evaluated.
        self.posttasks = []

    def add_problem(self, problem:Problem):
        if not isinstance(problem, Problem):
            raise TypeError("add_problem: Given arg should be Problem instance")
        self.problems.append(problem)
    
    def add_pretask(self, task:Task):
        if not isinstance(task, Task):
            raise TypeError("add_pretask: Given arg should be Task instance")
        self.pretasks.append(task)

    def add_posttask(self, task:Task):
        if not isinstance(task, Task):
            raise TypeError("add_posttask: Given arg should be Task instance")
        self.posttasks.append(task)
