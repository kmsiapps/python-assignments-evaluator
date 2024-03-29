import os
import argparse
import time
import re

from core.evaluate import Evaluator, Comparator
from core.writer import HTMLWriter, CSVWriter
from core.name_standardize import Extractor

'''
YCS1001 자동 채점 스크립트
author: hanju.yoo@yonsei.ac.kr
version: 2.1.0 (2022-05-24)
'''

def main():
    start_time = time.time()

    parser = argparse.ArgumentParser(description='YCS1001 Python problem evaluator')
    parser.add_argument('labname', type=str, help='채점할 주차명 (e.g. Lab1)')
    parser.add_argument('--file', type=str, nargs='*', required=False, help='채점할 파일명 (e.g. p2 p4)')
    parser.add_argument('--case', type=int, nargs='*', required=False, help='각 파일별 테스트 케이스 개수 (e.g. 4 3)')

    parser.add_argument('--unzip-code', default=False, action='store_true', help='LearnUs 압축파일에서 코드 추출 여부')
    parser.add_argument('--ignore-blanks', default=False, action='store_true', help='정답 비교 시 Whitespace(\\t, \\n, 공백) 무시')
    parser.add_argument('--ignore-capitals', default=False, action='store_true', help='정답 비교 시 대/소문자 구분 안 함')
    parser.add_argument('--timeout', type=float, default=5, help='최대 실행 시간')
    parser.add_argument('--thread', type=int, default=32, help='최대 스레드 수')

    args = parser.parse_args()
    labname = args.labname

    file = args.file
    case = args.case

    if not file:
        file_list = os.listdir(os.path.join(os.getcwd(), 'labs', labname, 'src'))
        file_list = filter(lambda f: re.findall(r'[^\/]+_in_\d+.txt', f), file_list)
        file_list = map(lambda f: f[:f.find('_')], file_list)
        file = list(set(file_list))
        file.sort()
    
    if not case:
        case = []
        for filename in file:
            file_list = os.listdir(os.path.join(os.getcwd(), 'labs', labname, 'src'))
            file_list = filter(lambda f: re.findall(f'{filename}_in_\\d+.txt', f), file_list)
            case_list = list(map(lambda f: int(f[f.rfind('_')+1:f.rfind('.')]), file_list))
            case_list.sort(reverse=True)
            maximum_case_num = case_list[0]
            case.append(maximum_case_num + 1) # as case num starts from zero

    files = tuple(map(lambda x, y: (x, y), file, case))
    print('info: using problem-cases pair as follows:')
    print(files)
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
