#!/usr/bin/env python3
#
# https://adventofcode.com/2018/
#
# AOC 2018 07
#
# aoc201807.py
#

print('# AOC 2018 07')

data = [ (s[5], s[36],) for s in """
Step G must be finished before step T can begin.
Step L must be finished before step V can begin.
Step D must be finished before step P can begin.
Step J must be finished before step K can begin.
Step N must be finished before step B can begin.
Step K must be finished before step W can begin.
Step T must be finished before step I can begin.
Step F must be finished before step E can begin.
Step P must be finished before step O can begin.
Step X must be finished before step I can begin.
Step M must be finished before step S can begin.
Step Y must be finished before step O can begin.
Step I must be finished before step Z can begin.
Step V must be finished before step Z can begin.
Step Q must be finished before step Z can begin.
Step H must be finished before step C can begin.
Step R must be finished before step Z can begin.
Step U must be finished before step S can begin.
Step E must be finished before step Z can begin.
Step O must be finished before step W can begin.
Step Z must be finished before step S can begin.
Step S must be finished before step C can begin.
Step W must be finished before step B can begin.
Step A must be finished before step B can begin.
Step C must be finished before step B can begin.
Step L must be finished before step P can begin.
Step J must be finished before step V can begin.
Step E must be finished before step W can begin.
Step Z must be finished before step W can begin.
Step W must be finished before step C can begin.
Step S must be finished before step W can begin.
Step Q must be finished before step S can begin.
Step O must be finished before step B can begin.
Step R must be finished before step W can begin.
Step D must be finished before step H can begin.
Step E must be finished before step O can begin.
Step Y must be finished before step H can begin.
Step V must be finished before step O can begin.
Step O must be finished before step S can begin.
Step X must be finished before step V can begin.
Step R must be finished before step E can begin.
Step S must be finished before step A can begin.
Step K must be finished before step Y can begin.
Step V must be finished before step W can begin.
Step U must be finished before step W can begin.
Step H must be finished before step R can begin.
Step P must be finished before step I can begin.
Step E must be finished before step C can begin.
Step H must be finished before step Z can begin.
Step N must be finished before step V can begin.
Step N must be finished before step W can begin.
Step A must be finished before step C can begin.
Step V must be finished before step E can begin.
Step N must be finished before step Q can begin.
Step Y must be finished before step V can begin.
Step R must be finished before step O can begin.
Step R must be finished before step C can begin.
Step L must be finished before step S can begin.
Step V must be finished before step R can begin.
Step X must be finished before step R can begin.
Step Z must be finished before step A can begin.
Step O must be finished before step Z can begin.
Step U must be finished before step C can begin.
Step X must be finished before step W can begin.
Step K must be finished before step O can begin.
Step O must be finished before step A can begin.
Step K must be finished before step T can begin.
Step N must be finished before step O can begin.
Step X must be finished before step C can begin.
Step Z must be finished before step C can begin.
Step N must be finished before step X can begin.
Step T must be finished before step A can begin.
Step D must be finished before step O can begin.
Step M must be finished before step Q can begin.
Step D must be finished before step C can begin.
Step U must be finished before step E can begin.
Step N must be finished before step H can begin.
Step I must be finished before step U can begin.
Step N must be finished before step A can begin.
Step M must be finished before step E can begin.
Step M must be finished before step V can begin.
Step P must be finished before step B can begin.
Step K must be finished before step X can begin.
Step N must be finished before step S can begin.
Step S must be finished before step B can begin.
Step Y must be finished before step W can begin.
Step K must be finished before step Q can begin.
Step V must be finished before step S can begin.
Step E must be finished before step S can begin.
Step N must be finished before step Z can begin.
Step P must be finished before step A can begin.
Step T must be finished before step V can begin.
Step L must be finished before step D can begin.
Step I must be finished before step C can begin.
Step Q must be finished before step E can begin.
Step Y must be finished before step U can begin.
Step J must be finished before step I can begin.
Step P must be finished before step H can begin.
Step T must be finished before step M can begin.
Step T must be finished before step E can begin.
Step D must be finished before step F can begin.
""".split('\n') if s ]

dataTest = [ (s[5], s[36],) for s in """
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
""".split('\n') if s ]
print(data)

def part1(data):
    """Part 1 of https://adventofcode.com/2018/day/7"""
    order = list()
    while data:
        prereq, inst = zip(*data)
        nextPrereq = [ p for p in prereq if p not in inst ]
        assert len(nextPrereq) > 0, \
            'no values in {} not in {}'.format(str(prereq), str(inst))
        c = sorted(nextPrereq)[0]
        order.append(c)
        if len(data) == 1:                         # add last job
            order.append(data[0][1])
        data = [ x for x in data if x[0] != c ]
    return ''.join(order)
print(part1(data))

def part2(data, n):
    """Part 2 of https://adventofcode.com/2018/day/7"""
    t = lambda c: ord(c) - ord('A') + 61            # time(char)
    e = lambda l: all([ x is None for x in l ])     # isEmpty(list)
    f = lambda l: None not in l                     # isFull(list)
    r = lambda d, c: [ x for x in d if x[0] != c ]  # remove(data, char)
    total, extra, jobs, durations, completed = 0, 0, [None] * n, [0] * n, []
    while data:
        prereq, inst = zip(*data)
        nextPrereq = sorted(set([ p for p in prereq if p not in inst ]))
        assert len(nextPrereq) > 0, \
            'no values in {} not in {}'.format(str(prereq), str(inst))
        # Process every job in prerequisite(s)
        for c in sorted(nextPrereq):
            if c not in jobs and None in jobs:
                # Add c and its duration
                i = durations.index(0)
                durations[i], jobs[i] = t(c), c,
        # Remove minimum value(s)
        minimum = min([ x for x in durations if x ])
        total, durations = total + minimum, [ max(0, x - minimum) for x in durations ]
        # Remove any newly completed jobs
        for i, d in enumerate(durations):
            if d == 0 and jobs[i] is not None:
                data, completed, jobs[i] = r(data, jobs[i]), completed + [jobs[i]], None
        if len(data) == 1:                          # add extra for last job
            extra = t(data[0][1])
    return total + max(durations) + extra
print(part2(data, 4))