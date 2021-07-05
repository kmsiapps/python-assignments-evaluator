class Task:
    def __init__(self, id:int, name:str, desc_text:str):
        self.id = id
        self.name = name
        self.desc_text = desc_text
        self.problem = None

    def run(self, working_dir:str):
        raise NotImplementedError()
    
    def wait(self, timeout:int):
        raise NotImplementedError()
