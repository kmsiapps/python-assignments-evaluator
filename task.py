from abc import abstractmethod, ABCMeta
import os
import subprocess
import re

from test import TestOutput, Test
from student import Student
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

    def build_task(self, task: DictWrapper):
        if not task.type in TaskBuilder.func_to_call:
            raise KeyError(f'Unknown task type: {task.type}')
        return TaskBuilder.func_to_call[task.type](task)
    
    def handle_Terminal(self, task: DictWrapper):
        return TerminalTask(self.directories, task)

    def handle_RegexReplace(self, task: DictWrapper):
        return RegexReplaceTask(self.directories, task)

    def handle_RunCmpFile(self, task: DictWrapper):
        return RunCmpFileTask(self.directories, task)

    def handle_RunCmpStdout(self, task: DictWrapper):
        return RunCmpStdoutTask(self.directories, task)


class Task(metaclass=ABCMeta):
    '''
    Defintion of tasks for evaluation tests
    '''
    def __init__(self, directories: dict, task: DictWrapper):
        '''
        directories: dict containing 'SOURCEDIR', 'CODEDIR'.
                     Used for supporting '$SOURCEDIR' or '$CODEDIR' alias
                     in task definitions.
        '''
        self.directories = directories
        self.type = task.type

    @abstractmethod
    def run(self, student: Student, test: Test):
        '''
        Run predefined task (e.g. Comparing outputs, ...)
        Tasks used for 'main task' should return (score, Diff)
        '''
        pass

    def __handle_special_directories(self, target_string: str):
        for special_dir, real_path in self.directories.items():
            if target_string and target_string.find('$' + special_dir) == 0:
                # only replace starting $SPECIALDIR 
                target_string = target_string.replace('$' + special_dir, real_path)
                break
        return target_string


class TerminalTask(Task):
    def __init__(self, directories: dict, task: DictWrapper):
        super.__init__(self, directories, task)
        self.inputs = (self.__handle_special_directories(dir) \
                       for dir in task.inputs)
        self.timeout = task.timeout
        self.terminal_alias = task.terminal_alias

    def run(self, student: Student, test: Test):
        for work in self.inputs:
            params_list = [self.terminal_alias] + work.split()
            # e.g ['cmd', 'cp', 'p1.py', 'p1_bak.py']
            p = subprocess.Popen(params_list)
            try:
                p.wait(timeout = self.timeout)
            except subprocess.TimeoutExpired:
                print(f'WARN: timeout during terminal operations({work})')
                p.kill()


class RegexReplaceTask(Task):
    def __init__(self, directories: dict, task: DictWrapper):
        super.__init__(self, directories, task)
        self.from_regex = task.from_regex
        self.to_string = task.to_string
        self.target_file = task.target_file
    
    def run(self, student: Student, test: Test):
        # Warning: maybe not thread-safe
        with open(f'{student.directory}/{self.target_file}', 'r+') as f:
            content = f.read()
            f.seek(0)
            f.truncate()
            f.write(re.sub(self.from_regex, self.to_string, content))


class RunCmpTask(Task):
    def __init__(self, directories: dict, task: DictWrapper):
        super.__init__(self, directories, task)
        self.interpreter_alias = task.interpreter_alias
        self.input_path = task.input_path
        self.output_path = task.output_path
        self.answer_path = task.answer_path
        self.ignore_capitals = task.ignore_capitals
        self.ignore_whitespaces = task.ignore_whitespaces
        self.target_file = task.target_file
        self.timeout = task.timeout

    def run(self, student: Student, test: Test):
        inputdir = self.input_path
        stdoutdir = os.path.join(student.directory, '{}_out_{}.txt'.format(self.target_file, test.name))
        errdir = os.path.join(student.directory, '{}_err_{}.txt'.format(self.target_file, test.name))
        filedir = os.path.join(student.directory, self.target_file)

        input_file = open(inputdir)
        stdout_file = open(stdoutdir, 'w')
        err_file = open(errdir, 'w')

        p = subprocess.Popen([self.interpreter_alias, filedir], 
                             stdin=input_file, stdout=stdout_file, stderr=err_file)

        inf_loop = False
        try:
            p.wait(timeout = self.timeout)
        except subprocess.TimeoutExpired:
            inf_loop = True
            p.kill()

        stdout_file.close()
        err_file.close()

        with open(filedir) as f:
            code = f.read()
        
        outputdir = self.get_output_path(stdoutdir)
        with open(outputdir) as f:
            output = f.read()
        
        with open(errdir) as f:
            err = f.read()

        # TODO
        test_out = TestOutput(student, test, code, output, err, inf_loop)
        return test.compare(test_out)

    @abstractmethod
    def get_output_path(self, stdoutdir: str):
        pass


class RunCmpFileTask(RunCmpTask):
    def __init__(self, directories: dict, task: DictWrapper):
        super.__init__(directories, task)
        self.output_path = task.output_path
        
    def get_output_path(self, stdoutdir: str):
        return self.output_path


class RunCmpStdoutTask(RunCmpTask):
    def __init__(self, directories: dict, task: DictWrapper):
        super.__init__(directories, task)
        
    def get_output_path(self, stdoutdir: str):
        return stdoutdir
