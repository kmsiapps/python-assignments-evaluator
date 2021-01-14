import os
import argparse
import time

from core.evaluate import Evaluator, Comparator
from core.writer import HTMLWriter, CSVWriter

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

    dirlist = tuple(
        _dir for _dir in os.listdir(os.path.join(os.getcwd(), 'labs', labname, 'codes')) \
        if os.path.isdir(os.path.join('labs', labname, 'codes', _dir)) \
    )

    comparator = Comparator(ignore_blanks=ignore_blanks,
                            ignore_capitals=ignore_capitals)
    evaluator = Evaluator(dirlist, labname, files, kill_timeout)
    evaluator.evaluate(comparator, n_thread)

    htmlwriter = HTMLWriter(f"labs/{labname}/result.html")
    evaluator.save(htmlwriter)

    csvwriter = CSVWriter(f"labs/{labname}/result.csv")
    evaluator.save(csvwriter)

    print("Evaluation done in {:.2f}s".format(time.time() - start_time))


if __name__ == "__main__":
    main()
