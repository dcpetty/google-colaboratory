#!/usr/bin/env python3
#
# test.py
#

"""Minimal test code for toy.py."""

from toy import TOY
from pathlib import Path

toy = TOY()

print('################################ TEST ################################')
print()

print('#' * 10, 'Assemble test.asm\n')
toy.asm(Path('test.asm'))
toy.listing()

print('############################## FIBONACCI #############################')
print()

print('#' * 10, 'Assemble fibonacci.asm\n')
toy.asm(Path('fibonacci.asm'))
toy.listing('fibonacci.toy')
toy.listing()

print('#' * 10, 'Run fibonacci.toy\n')
toy.run( 0x40 )
