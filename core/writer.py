import csv
from core.score_definition import *

class Writer:
    def __init__(self, filename):
        self.filename = filename
        self.content = ''

    def write(self, results):
        self.__save()
        
    def __save(self):
        pass


class HTMLWriter(Writer):
    def to_html_char(self, string):
        return string.replace('<', '&lt;').replace('>', '&gt;')
    
    def write(self, results):
        acc = []
        acc.append('<div class="body-wrapper">')
        for individuals in results:
            acc.append('<div class="student-box">')
            acc.append(f'<h3 class="student-no">{individuals.get_name()}</h3>')
            for problem in individuals:
                acc.append('<div class="problem-box">')
                if individuals[problem].perfect():
                    label_suffix = 'success'
                    show_details = False
                else:
                    label_suffix = 'warning'
                    show_details = True
                acc.append(f'<h4 class="problem-no">{problem}' +
                           '<span class="problem-score label label-{}">{:.2f}/{}'.format(
                                         label_suffix, individuals[problem].get_score()/PROBLEM_MAX_SCORE, individuals[problem].length()) +
                            '</span></h4>')
                if (show_details):
                    acc.append('<div class="problem-details">')
                    code = None
                    for case_idx, case in enumerate(individuals[problem]):
                        score, reason, diff, ans, __code, err = individuals[problem][case]
                        if __code:
                            code = __code
                        if (score == 3):
                            continue
                        acc.append(f'<div class="problem-result"><span class="label label-danger">#{case_idx} {reason}</span></div>')
                        if (diff):
                            acc.append(f'<pre class="diff-box">{diff.to_html()}</pre>')
                        if (ans):
                            acc.append(f'<pre class="ans-box">{ans}</pre>')
                        if (err):
                            acc.append(f'<pre class="alert alert-danger">{self.to_html_char(err)}</pre>')
                    if (code):
                        acc.append(f'<details><summary>코드 보기</summary><pre class="code-box">{self.to_html_char(code)}</pre></details>')
                    acc.append('</div>')
                acc.append('</div>')
            acc.append('<hr></div>')
        acc.append('</div>')
        acc.append('</body></html>')
        
        self.content += '\n'.join(acc)
        self.__save()
    
    def __save(self):
        content = \
'''<html><head><link rel="stylesheet" type="text/css" href="../../static/style.css">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css"></head><body>'''

        content += self.content
        content += '</body></html>'

        with open(self.filename, 'w') as f:
            f.write(content)


class CSVWriter(Writer):
    def write(self, results):
        self.content = []

        if len(results) == 0:
            return
        
        problem_lsts = list((key, results[0][key].length()) for key in results[0])
        # ['학번', '총점', 'P1', 'P1 #0', ..., 'P1 #N', 'P2', 'P2 #0', ..., 'P2 #M', '감점 사유']
        header = ['학번', '총점']
        for problem_idx, total_cases in problem_lsts:
            header.append(f'{problem_idx}')
            for case_num in range(total_cases):
                header.append(f'{problem_idx} #{case_num}')
        header += ['감점 사유']

        self.content.append(header)
        for individuals in results:
            content = [individuals.get_name()] # 학번

            total_scores = list(individuals[problem].get_score(max_score=1) for problem in individuals)
            content += [sum(total_scores) / len(total_scores) / PROBLEM_MAX_SCORE * TOTAL_MAX_SCORE] #총점

            reasons = []
            for problem in individuals:
                content += [individuals[problem].get_score()] # Pn 총점
                for case in individuals[problem]:
                    score, reason, _, _, _, _ = individuals[problem][case]
                    content.append(score)
                    if reason:
                        reason_string = f'{problem}: {reason}'
                        if reason_string not in reasons:
                            reasons.append(reason_string)
            
            content.append(', '.join(reasons)) # 감점사유
            self.content.append(content)
                
        self.__save()

    def __save(self):
        content = self.content
        with open(self.filename,'w', newline='') as f:
            wr = csv.writer(f)
            for x in content:
                wr.writerow(x)
