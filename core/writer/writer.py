import csv
from core.score_definition import *

class Writer:
    def __init__(self, filename):
        self.filename = filename
        self.content = ''

    def write(self, results):
        '''
        Append results to writer.
        results: list of Result object
        '''
        self.__save()
        
    def __save(self):
        '''
        Save results to file.
        '''
        pass
