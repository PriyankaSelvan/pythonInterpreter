from subprocess import *
import sys

output = Popen(["python", "python_interpreter.py", "ex1.py"], stdout=PIPE).communicate()[0]
answers = output.split()
print answers
actual = ['4', '6', '10', '12']
for i in range(0,4):
    if answers[i]!=actual[i]:
       sys.exit("Error at print statement "+str(i+1))
