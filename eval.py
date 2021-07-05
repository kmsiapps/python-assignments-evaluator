import os
import argparse
import time

from core.student import Student
from core.submission import Submission
from core.problem import Problem
from core.definition.task_type import OutputType
from core.task.runpy import RunPyTask
from core.utils.name_standardize import Extractor

'''
YCS1001 자동 채점 스크립트
author: hanju.yoo@yonsei.ac.kr
version: 2.0.0 (2020-08-28)
'''

def main():
    start_time = time.time()

    parser = argparse.ArgumentParser(description='YCS1001 Python problem evaluator')
    parser.add_argument('labname', type=str, help='채점할 주차명 (e.g. Lab1)')
    parser.add_argument('--file', type=str, nargs='*', required=True, help='채점할 파일명 (e.g. p2 p4)')
    parser.add_argument('--case', type=int, nargs='*', required=True, help='각 파일별 테스트 케이스 개수 (e.g. 4 3)')

    parser.add_argument('--unzip-code', default=False, action='store_true', help='LearnUs 압축파일에서 코드 추출 여부')
    parser.add_argument('--ignore-blanks', default=True, action='store_true', help='정답 비교 시 Whitespace(\\t, \\n, 공백) 무시')
    parser.add_argument('--ignore-capitals', default=True, action='store_true', help='정답 비교 시 대/소문자 구분 안 함')
    parser.add_argument('--timeout', type=int, default=5, help='최대 실행 시간')
    parser.add_argument('--thread', type=int, default=32, help='최대 스레드 수')

    args = parser.parse_args()
    labname = args.labname
    files = tuple(map(lambda x, y: (x, y), args.file, args.case))
    # e.g. (('p1', 3), ('p2' ,4))

    ignore_blanks = args.ignore_blanks
    ignore_capitals = args.ignore_capitals
    kill_timeout = args.timeout
    n_thread = args.thread

    if args.unzip_code:
        if os.path.exists(f'labs/{labname}/codes'):
            print(f'labs/{labname}/codes folder exists - aborting extraction')
        else:
            ext = Extractor(f'labs/{labname}.zip', f'labs/{labname}/codes')
            ext.run()
            print(f'Extraction done in {time.time() - start_time:.2f}s')
            start_time = time.time()

    dirlist = (
        _dir for _dir in os.listdir(os.path.join(os.getcwd(), 'labs', labname, 'codes')) \
        if os.path.isdir(os.path.join('labs', labname, 'codes', _dir)) \
    )

    '''
    Initial test code
    '''

    submission_lst = []
    for dir in dirlist:
        student = Student('John doe', dir)
        submission = Submission(os.path.join(os.getcwd(), 'labs', labname, 'codes', dir), student)
        problem = Problem('p2', {})
        problem.add_tasks(RunPyTask(0, 'foo foo', 'Prints "foo foo".',
                                       os.path.join(os.getcwd(), 'labs', labname, 'codes', dir, 'p2.py'),
                                       os.path.join(os.getcwd(), 'labs', labname, 'src', 'p2_ans_0.txt'),
                                       os.path.join(os.getcwd(), 'labs', labname, 'codes', dir, 'p2_out_0.txt'),
                                       os.path.join(os.getcwd(), 'labs', labname, 'codes', dir, 'p2_err_0.txt'),
                                       OutputType.STDOUT
                                       ))
        problem.add_tasks(RunPyTask(1, 'bar foo', 'Prints "bar foo".',
                                       os.path.join(os.getcwd(), 'labs', labname, 'codes', dir, 'p2.py'),
                                       os.path.join(os.getcwd(), 'labs', labname, 'src', 'p2_ans_1.txt'),
                                       os.path.join(os.getcwd(), 'labs', labname, 'codes', dir, 'p2_out_1.txt'),
                                       os.path.join(os.getcwd(), 'labs', labname, 'codes', dir, 'p2_err_1.txt'),
                                       OutputType.STDOUT
                                       ))
        submission.add_problem(problem)
        problem = Problem('p4', {})
        problem.add_tasks(RunPyTask(0, 'bar', 'Prints "bar".',
                                       os.path.join(os.getcwd(), 'labs', labname, 'codes', dir, 'p4.py'),
                                       os.path.join(os.getcwd(), 'labs', labname, 'src', 'p4_ans_0.txt'),
                                       os.path.join(os.getcwd(), 'labs', labname, 'codes', dir, 'p4_out_0.txt'),
                                       os.path.join(os.getcwd(), 'labs', labname, 'codes', dir, 'p4_err_0.txt'),
                                       OutputType.STDOUT
                                       ))
        submission.add_problem(problem)
        submission_lst.append(submission)
    
    for s in submission_lst:
        for p in s.problems:
            for t in p.tasks:
                t.run(os.path.join(os.getcwd(), 'labs', labname, 'codes', s.student.id))
                t.wait(3)
    
    print("Evaluation done in {:.2f}s".format(time.time() - start_time))


if __name__ == "__main__":
    main()
