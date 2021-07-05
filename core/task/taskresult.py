from core.task.task import Task
from core.task.types import ResultStatus

class TaskResult:
    '''
    TaskResult Class.
    Created in result of Task.run()
    task: Task instance
    status: ResultStatus instance (Represents Task execution status)
    output: Task output string
    err: Task error string
    '''
    def __init__(self, task:Task, status:ResultStatus, output:str, err:str):
        self.task = task
        self.status = status
        self.output = output
        self.err = err
