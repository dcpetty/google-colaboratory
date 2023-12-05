#!/usr/bin/env python3
#
# https://adventofcode.com/2018/
#
# AOC 2018 06
#
# aoc201806.py
#

print('# AOC 2018 06')

data = [ (int(x), int(y),) for x, y in [ s.split(',') for s in """
59, 110
127, 249
42, 290
90, 326
108, 60
98, 168
358, 207
114, 146
242, 170
281, 43
233, 295
213, 113
260, 334
287, 260
283, 227
328, 235
96, 259
232, 177
198, 216
52, 115
95, 258
173, 191
156, 167
179, 135
235, 235
164, 199
248, 180
165, 273
160, 297
102, 96
346, 249
176, 263
140, 101
324, 254
72, 211
126, 337
356, 272
342, 65
171, 295
93, 192
47, 200
329, 239
60, 282
246, 185
225, 324
114, 329
134, 167
212, 104
338, 332
293, 94
""".split('\n') if s ] ]
print(data)

dataTest = [ (int(x), int(y),) for x, y in [ s.split(',') for s in """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
""".split('\n') if s ] ]
print(data)

def dist(p1, p2):
    """Return Manhattan distance between p1 & p2."""
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2 - x1) + abs(y2 - y1)
def isFinite(i, x, y, space):
    """Return True if i, the valus of the xth row and yth column of space does not extend to any edge."""
    assert space[x][y] == i, '{} is not space[{}][{}] ({})'.format(i, x, y, str(space))
    return space[x][0] != i and space[x][len(space[x]) - 1] != i and space[0][y] != i and space[len(space) - 1][y] != i
def part1(data):
    """Part 1 of https://adventofcode.com/2018/day/6"""
    xs, ys = zip(*data)
    minX, maxX, minY, maxY = min(xs), max(xs), min(ys), max(ys)
    print(minX, maxX, minY, maxY)
    space = [ [ 0 ] * (maxY - minY + 1) for row in range(maxX - minX + 1) ]
    for x in range(minX, maxX + 1):
        for y in range(minY, maxY + 1):
            ds = [ dist(p, (x, y,)) for p in data ]
            space[x - minX][y - minY] = ds.index(min(ds)) if len([ d for d in ds if d == min(ds) ]) == 1 else None
            #for r in space: print([ '.' if c is None else chr(c + ord('A')) for c in r ])
            #print()
    return max([ len([ n for n in sum(space, []) if n == i ]) 
        for i, p in enumerate(data) if isFinite(i, p[0] - minX, p[1] - minY, space) ])
print(part1(data))

def part2(data):
    """Part 2 of https://adventofcode.com/2018/day/6"""
    xs, ys = zip(*data)
    minX, maxX, minY, maxY = min(xs), max(xs), min(ys), max(ys)
    short = [ sum([ dist(p, (x, y,)) for p in data ]) for x in range(minX, maxX + 1) for y in range(minY, maxY + 1) ]
    return len([ t for t in short if t < 10000 ])
print(part2(data))
