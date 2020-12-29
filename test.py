from dictwrapper import DictWrapper
from student import Student
from evaluate import Diff
from task import TaskBuilder

class Test:
    '''
    Class for test definition, such as name, points, etc.
    '''
    def __init__(self, definition: dict, taskbuilder: TaskBuilder):
        self.name = definition['name']
        self.desc = definition['desc']
        self.mandatory = definition['mandatory']
        self.main_task = definition['main_task']
        self.tasks = self.build_task(definition, TaskBuilder)
    
    def build_task(self, definition: dict, taskbuilder: TaskBuilder):
        definition = DictWrapper(definition)
        return [taskbuilder.build_task(task) for task in definition.tasks]
     
    def run(self):
        # TODO: return TestExec
        pass

    def compare(self, test_exec: TestExec):
        # TODO: compare self and test_exec => TestResult
        pass

class TestExec:
    '''
    Test execution result class which consists output, err, etc.
    '''
    def __init__(self, student: Student, test: Test,
                 code: str, output: str, err: str,
                 inf_loop:bool = False):
        self.test = test
        self.student = student
        self.output = output
        self.err = err
        self.inf_loop = inf_loop
        self.code = code

class TestResult:
    '''
    Test evaluation result class which consists diff, score, etc.
    '''
    def __init__(self, test: Test, test_exec: TestExec, score: float,
                 diff: Diff, reason: str):
        self.test_exec = test_exec
        self.score = 0
        self.diff = diff
        self.reason = reason
