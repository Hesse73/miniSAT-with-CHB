from z3 import *
import sys
import time

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('py ./z3sat.py <input-file>')
    else:
        contents = open(sys.argv[1], 'r').readlines()
        cnf = []
        for line in contents:
            if line[0] == 'c':
                continue
            if line[0] == 'p':
                v_num = int(line.split(' ')[2])
                X = [Bool('x_%d' % i) for i in range(1, v_num+1)]
                continue
            line_constr = []
            for v in line.split(' '):
                if v[0] == '0':
                    break
                if v[0] == '-':
                    line_constr.append(Not(X[int(v[1:]) - 1]))
                if v[0] in ['%d' % i for i in range(10)]:
                    line_constr.append(X[int(v) - 1])
            if len(line_constr) > 0:
                cnf.append(Or(line_constr))
        start = time.perf_counter()
        s = Solver()
        s.add(And(cnf))
        res = s.check()
        end = time.perf_counter()
        print('Time Elapsed:', end-start)
        print('Result:', res)
