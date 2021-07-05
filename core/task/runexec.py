from enum import Enum, auto

import subprocess, os
from core.task.task import Task
from core.task.types import ResultStatus
from core.task.taskresult import TaskResult

class OutputType(Enum):
    STDOUT = auto()
    FILE = auto()

class RunExecutableTask(Task):
    def __init__(self, id:int, name:str, desc_text:str,
                 interpreter:str, input_dir:str, ans_dir:str,
                 file_dir:str, output_dir:str, err_dir:str,
                 output_type: OutputType,timeout:int):
        super().__init__(id, name, desc_text)

        self.input_dir = input_dir
        self.output_dir = output_dir
        self.err_dir = err_dir
        self.file_dir = file_dir
        self.interpreter = interpreter
        self.timeout = timeout
        
        self.status = ResultStatus.PENDING
        self.result = None

        f = open(ans_dir)
        self.ans = f.read()
        f.close()
        
        if not isinstance(output_type, OutputType):
            raise TypeError(f"RunPyTask::run: unknown output type {output_type}")
        self.output_type = output_type
    
    def run(self, working_dir:str):
        working_dir = os.path.abspath(working_dir)

        if not os.path.exists(self.file_dir):
            self.status = ResultStatus.FILE_NOT_FOUND
        
        self.input_f = open(self.input_dir, 'r')
        self.err_f = open(self.err_dir, 'w')

        if self.output_type == OutputType.STDOUT:
            self.output_f = open(self.output_dir, 'w')
            self.process = subprocess.Popen([self.interpreter, self.file_dir],
                                            stdin=self.input_f,
                                            stdout=self.output_f,
                                            stderr=self.err_f,
                                            cwd=working_dir)
        else:
            self.process = subprocess.Popen([self.interpreter, self.file_dir],
                                            stdin=self.input_f,
                                            stderr=self.err_f,
                                            cwd=working_dir)

    def wait(self):
        if not self.status == ResultStatus.PENDING:
            return
        
        try:
            self.process.wait(timeout = self.timeout)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.input_f.close()
            self.err_f.close()
            if self.output_type == OutputType.STDOUT:
                self.output_f.close()
            self.status = ResultStatus.INF_LOOP

    def get_result(self):
        if not self.result:
            with open(self.output_dir, 'r') as f:
                output = f.read()
            with open(self.err_dir, 'r') as f:
                err = f.read()
            
            if err:
                self.status = ResultStatus.RUNTIME_ERR
            elif output != self.ans:
                self.status = ResultStatus.OUTPUT_MISMATCH
            else:
                self.status = ResultStatus.SUCCESS
            
            self.result = TaskResult(self, self.status, output, err)
        
        return self.result
