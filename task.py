from abc import *

from dictwrapper import DictWrapper

class TaskBuilder:
    '''
    Builds tasks from dictionary
    '''
    func_to_call = {
        'Terminal': handle_Terminal,
        'RegexReplace': handle_RegexReplace,
        'RunCmpFile': handle_RunCmpFile,
        'RunCmpStdout': handle_RunCmpStdout,
    }

    def __init__(self, directories: dict):
        '''
        directories: dict containing 'SOURCEDIR', 'CODEDIR'.
                     Used for supporting '$SOURCEDIR' or '$CODEDIR' alias
                     in task definitions.
        '''
        self.directories = directories

    @staticmethod
    def build_task(task: DictWrapper):
        if not task.type in TaskBuilder.func_to_call:
            raise KeyError(f'Unknown task type: {task.type}')
        return TaskBuilder.func_to_call[task.type](task)
    
    @staticmethod
    def handle_Terminal(task: DictWrapper):
        pass

    @staticmethod
    def handle_RegexReplace(task: DictWrapper):
        pass

    @staticmethod
    def handle_RunCmpFile(task: DictWrapper):
        pass

    @staticmethod
    def handle_RunCmpStdout(task: DictWrapper):
        pass
    
class Task(metaclass=ABCMeta):
    '''
    Defintion of tasks for evaluation tests
    '''
    def __init__(self, directories: dict):
        '''
        directories: dict containing 'SOURCEDIR', 'CODEDIR'.
                     Used for supporting '$SOURCEDIR' or '$CODEDIR' alias
                     in task definitions.
        '''
        self.directories = directories

    @abstractmethod
    def run(self):
        '''
        Run predefined task (e.g. Comparing outputs, ...)
        Tasks used for 'main task' should return (score, Diff)
        '''
        pass

class TerminalTask(Task):
    pass

class RegexReplaceTask(Task):
    pass

class RunCmpTask(Task):
    pass

class RunCmpFileTask(RunCmpTask):
    pass

class RunCmpStdoutTask(RunCmpTask):
    pass
