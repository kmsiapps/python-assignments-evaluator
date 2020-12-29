from difflib import SequenceMatcher
import re

from test import TestResult

class Evaluator:
    # Evaluate Student
    
    # Test.run() and Test.compare() => ProbResult
    # ProbResults => Student
    def evaluate(self, test, test_exec):
        result_type = ''
        result_str = ''
        diff = None

        if test_exec.inf_loop:
            result_type = 'inf_loop'

        if not result_type:
            # Check required keywords
            required_kwd = test.required_keywords
            for k in required_kwd:
                if k not in test_exec.code:
                    result_type = 'kwd_required'
                    result_str = k
                    break
        
        if not result_type:
            # Check banned keywords
            banned_kwd = test.banned_keywords
            for k in banned_kwd:
                match = re.findall(f'\\b{k}\\b', test_exec.code)
                if match:
                    result_type = 'kwd_banned'
                    result_str = k
                    break
        
        if not result_type:
            output = test_exec.output
            desired_output = test.desired_output

            if test.options['ignore_capitals']:
                output = output.lower()
                desired_output = desired_output.lower()
            if test.options['ignore_whitespaces']:
                output = ''.join(output.split())
                desired_output = ''.join(desired_output.split())

            if desired_output == output:
                result_type = 'correct'
            else:
                result_type = 'mistmatch'
                diff = self.buildDiff(test, test_exec)

        score, reason = self.buildScore(test, result_type, result_str)
        return TestResult(test, test_exec, score, diff, reason)

    def buildDiff(self, test, test_exec):
        ans = test.desired_output
        target = test_exec.code

        if test.options['ignore_capitals']:
            _ans = ans.lower()
            _target = target.lower()

        junk_func = lambda x: x.isspace() if test.options['ignore_whitespaces'] else None
        match = SequenceMatcher(junk_func, _ans, _target).get_opcodes()

        # TODO: if junk_func does not work, filter match
        return Diff(ans, target, match)

    def buildScore(self, test, result_type, result_str):
        if result_type == 'correct':
            score = test.points['correct']
            reason = ''
        elif result_type == 'inf_loop':
            score = test.points['infinite_loop']
            reason = '무한루프'
        elif result_type == 'kwd_banned':
            score = 0
            reason = f'금지 키워드 사용({result_str})'
        elif result_type == 'kwd_required':
            score = 0
            reason = f'필수 키워드 미사용({result_str})'
        elif result_type == 'mismatch':
            score = test.points['output_mismatch']
            reason = '실행 결과 불일치'
        else:
            raise ValueError(f"Unknown result type: {result_type}")

        if reason:
            reason = f'{test.name}: {reason}'
        return score, reason


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
