import re
import os
import subprocess
from difflib import SequenceMatcher
from core.score_definition import *

from core.writer import HTMLWriter, CSVWriter

class Result:
    def __init__(self, filename):
        self.name = filename
        self.container = {}
    
    def __iter__(self):
        return self.container.__iter__()
    
    def __getitem__(self, key):
        return self.container.__getitem__(key)
    
    def __setitem__(self, key, value):
        return self.container.__setitem__(key, value)
    
    def get_score(self, max_score=None):
        scores_lst = list(self.container[k][0] for k in self.container.keys())
        scores = sum(scores_lst)
        if (max_score):
            scores = scores / len(scores_lst) * max_score
        return scores

    
    def length(self):
        return len(self.container)
    
    def perfect(self):
        return self.get_score() == 3 * self.length()


class ResultContainer:
    def __init__(self, name):
        self.name = self.__prettify_name(name)
        self.result = {}

    def __prettify_name(self, name):
        regex = re.compile(r'20\d{8}')   
        stu_num = re.findall(regex, name)
        stu_num = name if len(stu_num) != 1 else stu_num[0]
        return stu_num
    
    def add_result(self, filename, case_idx, score, reason="", diff=None, ans=None, code=None, err=None):
        if filename not in self.result:
            self.result[filename] = Result(filename)

        self.result[filename][case_idx] = (score, reason, diff, ans, code, err)
    
    def get_score(self, max_score=None):
        total_score = 0
        for filename in self.result:
            problem = self.result[filename]
            total_score += problem.get_scores(max_score=1)

        if (max_score):
            total_score = total_score / len(self.result) * max_score
        
        return total_score
    
    def __iter__(self):
        return self.result.__iter__()

    def __getitem__(self, item):
        return self.result.__getitem__(item)
    
    def length(self):
        return len(self.result)
    
    def get_name(self):
        return self.name


class Evaluator:
    def __init__(self, dirs, labname, files, kill_timeout):
        self.dirs = dirs
        self.files = files
        self.results = []
        self.labname = labname
        self.kill_timeout = kill_timeout
    
    def __run(self, filepath, inputdir, outputdir, errdir, kill_timeout):
        try:
            input_file = open(inputdir, 'r')
            output_file = open(outputdir, 'w')
            err_file = open(errdir, 'w')
            p = subprocess.Popen(['python', filepath], stdin=input_file, stdout=output_file, stderr=err_file)
            p.wait(timeout = kill_timeout)
        except subprocess.TimeoutExpired:
            p.kill()
            input_file.close()
            output_file.close()
            raise TimeoutError
        
        input_file.close()
        output_file.close()

        with open(outputdir) as f:
            output = f.read()

        with open(errdir) as f:
            err = f.read()
        
        return output, err

    def evaluate(self, comparator):
        rootdir = os.path.join(os.getcwd(), 'labs', self.labname)
        for dir in self.dirs:
            result = ResultContainer(dir)
            for filename, num_case in self.files:
                filepath = os.path.join(rootdir, 'codes', dir, filename + ".py")
                banned_kwd_dir = os.path.join(rootdir, 'src', "{}_ban_keyword.txt".format(filename))
                required_kwd_dir = os.path.join(rootdir, 'src', "{}_req_keyword.txt".format(filename))

                try:
                    with open(filepath, encoding='utf-8') as f:
                        codes = ''.join(f.readlines())
                except:
                    # No code exists
                    for case_idx in range(num_case):
                        result.add_result(filename, case_idx, NO_FILE_SCORE, "파일 미제출")
                    continue

                try:
                    with open(banned_kwd_dir) as f:
                        banned = f.readlines()
                except:
                    banned = []

                try:
                    with open(required_kwd_dir) as f:
                        required = f.readlines()
                except:
                    required = []
                
                for kwd in banned:
                    if kwd.strip() in codes:
                        for case_idx in range(num_case):
                            result.add_result(filename, case_idx, BANNED_KWD_SCORE, f"금지 키워드({kwd}) 사용", code=codes)
                        continue
                
                for kwd in required:
                    if kwd.strip() not in codes:
                        for case_idx in range(num_case):
                            result.add_result(filename, case_idx, NO_REQUIRED_KWD_SCORE, f"필수 키워드({kwd}) 미사용", code=codes)
                        continue

                for case_idx in range(num_case):
                    inputdir = os.path.join(rootdir, 'src', '{}_in_{}.txt'.format(filename, case_idx))
                    outputdir = os.path.join(rootdir, 'codes', dir, '{}_out_{}.txt'.format(filename, case_idx))
                    errdir = os.path.join(rootdir, 'codes', dir, '{}_err_{}.txt'.format(filename, case_idx))
                    ansdir = os.path.join(rootdir, 'src', "{}_ans_{}.txt".format(filename, case_idx))

                    with open(ansdir) as f:
                        ans = f.read()
                    
                    try:
                        target, err = self.__run(filepath, inputdir, outputdir, errdir, self.kill_timeout)
                    except TimeoutError:
                        result.add_result(filename, case_idx, INF_LOOP_SCORE, f"무한루프(실행 시간 {self.kill_timeout}s 초과)", code=codes)
                        continue

                    diff = comparator.get_diff(ans, target)
                    if (diff == None):
                        result.add_result(filename, case_idx, PROBLEM_MAX_SCORE)
                    elif err:
                        result.add_result(filename, case_idx, STDOUT_ERR_SCORE, "실행 중 오류 발생", diff=diff, ans=ans, code=codes, err=err)
                    else:
                        result.add_result(filename, case_idx, INTERPRET_ERR_SCORE, "실행 결과 불일치", diff=diff, ans=ans, code=codes) # 일반적으로 2점
            
            self.results.append(result)
    
    def save(self, writer):
        writer.write(self.results)


class Comparator:
    def __init__(self, ignore_blanks = True, ignore_capitals = True):
        self.diff = ()
        self.ignore_blanks = ignore_blanks
        self.ignore_capitals = ignore_capitals

    def get_diff(self, ans, target):
        _ans = ans
        _target = target
        if self.ignore_blanks:
            _ans = "".join(_ans.split())
            _target = "".join(_target.split())
        if self.ignore_capitals:
            _ans = _ans.lower()
            _target = _target.lower()
        
        if (_ans == _target):
            return None

        junk_func = None
        if self.ignore_blanks:
            junk_func = lambda x: x in " \t\n"
        
        if self.ignore_capitals:
            _ans = ans.lower()
            _target = target.lower()

        return Diff(ans, target, SequenceMatcher(junk_func, _ans, _target).get_opcodes())


class Diff:
    def __init__(self, ans, target, match):
        self.match = match
        self.ans = ans
        self.target = target
    
    def to_html(self):
        acc = []

        for tag, i1, i2, j1, j2 in self.match:
            if tag == 'delete':
                string = self.ans[i1:i2]
            else:
                string = self.target[j1:j2]

            # Show as \n, not newline character
            if string == "\n" and tag != 'equal':
                string = "\\n"
            string.replace('\n', '</br>')
            
            acc.append(f'<span class="tag-{tag}">{string}</span>')

        return ''.join(acc)
