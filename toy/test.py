#!/usr/bin/env python3
#
# test.py
#

"""Minimal test code for toy.py."""

from toy import TOY


print('################################ TEST ################################')
print()

toy = TOY()

print('#' * 10, 'Assemble test.asm\n')
with open('test.asm', 'r') as f:
    toy.asm(f.readlines())
toy.listing()

print('#' * 10, 'Assemble fibonacci.asm\n')
with open('fibonacci.asm', 'r') as f:
    toy.asm(f.readlines())
toy.listing()
toy.listing('fibonacci.toy')

print('#' * 10, 'Run fibonacci.toy\n')
toy.run( 0x40 )
