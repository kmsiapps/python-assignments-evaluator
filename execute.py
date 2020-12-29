import os
import subprocess

from test import TestExec

class Executor:
    # TODO: UNNCECESSARY?
    def __init__(self, num_thread=8):
        pass

    def run(self, filedir, student, test):
        # run file
        # get err and output, based on tasks
        # return TestExec(self, output, err)
        path, filename = os.path.split(os.path.realpath(filedir))
        #inputdir = os.path.join(rootdir, 'src', '{}_in_{}.txt'.format(filename, case_idx))
        outputdir = os.path.join(path, '{}_out_{}.txt'.format(filename, test.name))
        errdir = os.path.join(path, '{}_err_{}.txt'.format(filename, test.name))

        output_file = open(outputdir, 'w')
        err_file = open(errdir, 'w')

        p = subprocess.Popen(['python', filedir], stdout=output_file, stderr=err_file)

        inf_loop = False
        try:
            p.wait(timeout = test.timeout)
        except subprocess.TimeoutExpired:
            inf_loop = True
            p.kill()

        output_file.close()
        err_file.close()

        with open(filedir) as f:
            code = f.read()
        
        with open(outputdir) as f:
            output = f.read()
        
        with open(errdir) as f:
            err = f.read()

        return TestExec(student, test, code, output, err, inf_loop)

