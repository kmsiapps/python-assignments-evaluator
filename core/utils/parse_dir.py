import os

from core.submission import Submission

def parse_dir(source:str, submission:Submission):
    source = source.replace('$SUBMISSIONDIR$', submission.directory)
    source = source.replace('$SOURCEDIR$', os.path.join(submission.directory, '../../src'))
    return source
