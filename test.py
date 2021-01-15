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
        self.tasks = self.__build_task(definition, TaskBuilder)
    
    def __build_task(self, definition: dict, taskbuilder: TaskBuilder):
        definition = DictWrapper(definition)
        return [taskbuilder.build_task(task) for task in definition.tasks]
    
    def compare(self, testoutput: TestOutput):
        # TODO
        # return TestResult
        pass


class TestContext:
    def __init__(self, test: Test, student: Student):
        self.test = test
        self.student = student
    
    def run(self):
        result = None
        for task in self.test.tasks:
            ret = task.run(self.student, self.test)
            if isinstance(ret, TestResult):
                result = ret
        
        if not result:
            raise ValueError('Test must include a task that returns TestResult')
        return result


class TestOutput:
    '''
    Test execution result class which consists output, err, etc.
    '''
    def __init__(self, student: Student, test: Test,
                 code: str, output: str, err: str,
                 inf_loop:bool = False):
        self.test = test
        self.output = output
        self.err = err
        self.inf_loop = inf_loop
        self.code = code


class TestResult:
    '''
    Test evaluation result class which consists diff, score, etc.
    '''
    def __init__(self, test: Test, test_output: TestOutput, score: float,
                 diff: Diff, reason: str):
        self.test_output = test_output
        self.score = 0
        self.diff = diff
        self.reason = reason
