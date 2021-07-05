from core.task.task import Task

class TaskResult:
    '''
    TaskResult Class.
    Created in result of Task.run()
    task: Task instance
    status: Task execution status
    output: Task output string
    err: Task error string
    '''
    def __init__(self, task:Task, status:str, output:str, err:str):
        self.task = task
        self.status = status
        self.output = output
        self.err = err
