from core.task.task import Task

class Problem:
    def __init__(self, name: str, score_def: dict):
        '''
        Problem class
        Represents a problem, including tests to evaluate it
        name: name of the problem (e.g. p1)
        score_def: error(key)-score(value) pairs
        tasks: Task instance, which represents test cases
               Each tasks runs in parallel
        '''
        self.name = name
        self.score_def = score_def
        self.tasks = []

    def add_tasks(self, task:Task):
        if not isinstance(task, Task):
            raise TypeError("add_tasks: Given arg should be Task instance")
        task.problem = self
        self.tasks.append(task)
    