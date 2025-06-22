#!/usr/bin/env python3
#
# https://adventofcode.com/2021/
#
# AOC 2021 06
#
# aoc202106.py
#

print('# AOC 2021 6')

data = [ int(x) for x in """
1,3,4,1,5,2,1,1,1,1,5,1,5,1,1,1,1,3,1,1,1,1,1,1,1,2,1,5,1,1,1,1,1,4,4,1,1,4,1,1,2,3,1,5,1,4,1,2,4,1,1,1,1,1,1,1,1,2,5,3,3,5,1,1,1,1,4,1,1,3,1,1,1,2,3,4,1,1,5,1,1,1,1,1,2,1,3,1,3,1,2,5,1,1,1,1,5,1,5,5,1,1,1,1,3,4,4,4,1,5,1,1,4,4,1,1,1,1,3,1,1,1,1,1,1,3,2,1,4,1,1,4,1,5,5,1,2,2,1,5,4,2,1,1,5,1,5,1,3,1,1,1,1,1,4,1,2,1,1,5,1,1,4,1,4,5,3,5,5,1,2,1,1,1,1,1,3,5,1,2,1,2,1,3,1,1,1,1,1,4,5,4,1,3,3,1,1,1,1,1,1,1,1,1,5,1,1,1,5,1,1,4,1,5,2,4,1,1,1,2,1,1,4,4,1,2,1,1,1,1,5,3,1,1,1,1,4,1,4,1,1,1,1,1,1,3,1,1,2,1,1,1,1,1,2,1,1,1,1,1,1,1,2,1,1,1,1,1,1,4,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,2,5,1,2,1,1,1,1,1,1,1,1,1
""".split(',') if x ]
print(data)

def part1(data):
    """Answer part 1 of https://adventofcode.com/2021/day/5"""
    for d in range(80):
        data = [ x - 1 for x in data ]
        new = len([ x for x in data if x < 0 ])
        data = [ x if x >= 0 else 6 for x in data ] + [8] * new
    return len(data)
print(part1(data))      # 386755

def part2(data):
    """Answer part 2 of https://adventofcode.com/2021/day/5"""
    sets = [ set() for i in range(9) ]
    for i, n in enumerate(data):
        sets[n].add(i)
    # print(sets)
    fish = [ len(s) for s in sets ]
    for d in range(256):
        eights = fish[0]
        sixes = eights + fish[7]
        fish = fish[1: ] + [eights]
        fish[6] = sixes
    return sum(fish)
print(part2(data))      # 1732731810807
