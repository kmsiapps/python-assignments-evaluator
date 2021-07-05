import subprocess, os
from core.task.task import Task
from core.definition.task_type import OutputType

class RunPyTask(Task):
    def __init__(self, id:int, name:str, desc_text:str,
                 file_dir:str, input_dir:str, output_dir:str,
                 err_dir:str, output_type: OutputType):
        super().__init__(id, name, desc_text)

        self.input_dir = input_dir
        self.output_dir = output_dir
        self.err_dir = err_dir
        self.file_dir = file_dir
        
        if not isinstance(output_type, OutputType):
            raise TypeError(f"RunPyTask::run: unknown output type {output_type}")
        self.output_type = output_type
    
    def run(self, working_dir:str):
        working_dir = os.path.abspath(working_dir)
        
        self.input_f = open(self.input_dir, 'r')
        self.err_f = open(self.err_dir, 'w')

        if self.output_type == OutputType.STDOUT:
            self.output_f = open(self.output_dir, 'w')
            self.process = subprocess.Popen(['python', self.file_dir],
                                            stdin=self.input_f,
                                            stdout=self.output_f,
                                            stderr=self.err_f,
                                            cwd=working_dir)
        else:
            self.process = subprocess.Popen(['python', self.file_dir],
                                            stdin=self.input_f,
                                            stderr=self.err_f,
                                            cwd=working_dir)

    def wait(self, timeout:int):
        try:
            self.process.wait(timeout = timeout)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.input_f.close()
            self.err_f.close()
            if self.output_type == OutputType.STDOUT:
                self.output_f.close()
        
        # TODO: save result object
    
    def get_result(self):
        return super().get_result()
