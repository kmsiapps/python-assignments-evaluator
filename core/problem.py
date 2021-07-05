from core.task.task import Task

class Problem:
    def __init__(self, name: str):
        '''
        Problem class
        Represents a problem, including tests to evaluate it
        name: name of the problem (e.g. p1)
        score_def: error(key)-score(value) pairs
        tasks: Task instance, which represents test cases
               Each tasks runs in parallel
        '''
        self.name = name
        self.student = None

        self.tasks = []

        # Tasks that are run beforehand. Executed in order.
        self.pretasks = []

        # Tasks which are executed in order,
        # after all problems are evaluated.
        self.posttasks = []
    
    def set_submission(self, submission):
        self.submission = submission

    def add_tasks(self, task:Task):
        if not isinstance(task, Task):
            raise TypeError("add_tasks: Given arg should be Task instance")
        task.set_problem(self)
        self.tasks.append(task)
    
    def add_pretask(self, task:Task):
        if not isinstance(task, Task):
            raise TypeError("add_pretask: Given arg should be Task instance")
        self.pretasks.append(task)

    def add_posttask(self, task:Task):
        if not isinstance(task, Task):
            raise TypeError("add_posttask: Given arg should be Task instance")
        self.posttasks.append(task)

    