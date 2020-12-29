import json

from evaluate import Evaluator
from test import Test, TaskBuilder
from execute import Executor
from student import Student

with open("test_example.json") as f:
    test_settings = json.loads(f.read())

# TODO: Implement Various Tasks
# TODO: Implement Test:run(), Test:compare()
# TODO: REWORK EXECUTOR AND EVALUATOR
ex = Executor()
ev = Evaluator()

# TODO: BUILD directories dict and pass it to TaskBuilder
tb = TaskBuilder({})
t = Test(test_settings, tb)

# TODO: PASS TESTRESULT TO PROBRESULT, AND FINALLY STUDENT
s = Student('hanju')
te = ex.run("./Lab1/codes/2020195154/p3.py", s, t)

tr = ev.evaluate(t, te)
