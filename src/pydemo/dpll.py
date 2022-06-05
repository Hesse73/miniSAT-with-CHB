from typing import Dict, List
import time
import sys

class Clause:
    def __init__(self, clause_dict: Dict[int, bool]):
        self.clause = clause_dict
        self.ids = [*self.clause]

    def isUnit(self):
        return len(self.clause) == 1

    def getLiteral(self):
        for k, v in self.clause.items():
            return (k, v)

    def removeLiteral(self, ids: List[int]):
        for id in ids:
            self.clause.pop(id)
            self.ids.remove(id)

    def copy(self):
        return Clause(self.clause)


def DPLL(unset_ids: List[int], clauses: List[Clause]):
    units = {}
    for C in clauses:
        if C.isUnit():
            lid, lsign = C.getLiteral()
            if lid in units and units[lid] != lsign:
                return False,None
            units[lid] = lsign
    #unit-resol
    for C in clauses:
        if C.isUnit():
            continue
        toremove = [
            id for id in C.ids if id in units and units[id] == C.clause[id]]
        if len(toremove) != 0:
            clauses.remove(C)
            continue
        toshrink = [
            id for id in C.ids if id in units and units[id] != C.clause[id]]
        if len(toshrink) != 0:
            C.removeLiteral(toshrink)
    #check if false with units
    for C in clauses:
        if not C.isUnit():
            sat = False
            for id, sign in C.clause.items():
                if (id not in units) or (id in units and sign == units[id]):
                    sat = True
                    break
            if not sat:
                return False,None
    #check if X is empty
    next_ids = [id for id in unset_ids if id not in units]
    if len(next_ids) == 0:
        return True,units
    #choose next_p
    next_p = next_ids[0]
    c_copy = [C.copy() for C in clauses]
    status,new_units = DPLL(next_ids, clauses+[Clause({1: True})])
    if status:
        for k,v in new_units.items():
            if k not in units:
                units[k] = v
        return True,units
    status,new_units = DPLL(next_ids, clauses+[Clause({1: False})])
    if status:
        for k,v in new_units.items():
            if k not in units:
                units[k] = v
        return True,units
    return False,None


if __name__ == '__main__':

    #sys.setrecursionlimit(20000)
    filename = input('input file path:')
    contents = open(filename, 'r').readlines()
    cnf = []
    unset_ids = []
    for line in contents:
        if line[0] == 'c':
            continue
        if line[0] == 'p':
            unset_ids = list(range(1, int(line.split(' ')[2])+1))
            continue
        line_dict = {}
        for v in line.split(' '):
            if v[0] == '0':
                break
            if v[0] == '-':
                line_dict[int(v[1:])] = False
            else:
                line_dict[int(v)] = True
        cnf.append(line_dict)
    clauses = []
    for c in cnf:
        clauses.append(Clause(c))
    start = time.perf_counter()
    status,units = DPLL(unset_ids, clauses)
    end = time.perf_counter()
    print('Time elapsed:', end-start)
    if status:
        print("SAT",units)
    else:
        print("UNSAT")