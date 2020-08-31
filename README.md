## YCS1001 Auto Evaluator

Usage: `python eval.py LABNAME --file p2 p4 --case 4 3 --ignore-blanks --ignore-capitals --timeout 5`

```
labs: 특정 주차의 채점용 파일들이 폴더로 들어 있습니다.
    Lab1/ : 주차명은 마음대로 해도 되지만, 프로그램 실행 시 입력해야 합니다.
        codes/ : 채점할 코드를 넣는 폴더입니다.
            Lab1/
                2018123456/
                    p1.py
                    p2.py
        src/ : 채점 시 필요한 답, 금지 키워드, 필수 키워드 등이 들어 있습니다.
            p1_in_0.txt : stdin에 입력되는 파일입니다. 입력 하나씩 엔터로 구분하여 적습니다.
                        pN_in_M 꼴로 적으면 됩니다. 이때 N은 문제 번호, M은 항상 0부터 시작하는 정수입니다.
            p1_in_1.txt
            p1_ban_keyword.txt : (선택) 코드 내 들어가면 안 되는 키워드를 정리해 둔 파일입니다. 키워드 하나씩 엔터로 구분하여 적습니다.
            p1_req_keyword.txt : (선택) 코드 내 반드시 들어가야 하는 키워드를 정리해 둔 파일입니다. 키워드 하나씩 엔터로 구분하여 적습니다.
            p1_ans_0.txt : stdout과 비교할 정답 출력 파일입니다. in 파일과 개수가 같아야 합니다.
            p1_ans_1.txt
            p2_in_0.txt
            p2_ans_0.txt
core/ : 본 채점 스크립트의 각종 모듈이 들어 있습니다.
    evaluate.py : 채점의 실행, 결과 관련 클래스들이 정의되어 있습니다.
    writer.py : HTMLWriter, CSVWriter 등 결과를 파일로 쓰는 클래스들이 정의되어 잇습니다.
static/ : result.html에 사용되는 css 파일 등 정적 파일이 들어 있습니다.
    style.css
result.html : 채점 완료 시 생성되는 보고서 html 파일입니다. 
result.csv : 채점 완료 시 생성되는 보고서 csv 파일입니다. 
```