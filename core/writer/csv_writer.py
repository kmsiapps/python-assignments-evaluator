import csv
from core.writer.writer import Writer
from core.score_definition import *

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
