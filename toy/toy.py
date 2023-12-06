#!/usr/bin/env python3
#
# toy.py
#

"""Simulator and assembler for the Princeton COS 126 TOY computer."""

import re

__author__ = "David C. Petty"
__copyright__ = "Copyright 2017, David C. Petty"
__license__ = "https://creativecommons.org/licenses/by-nc-sa/4.0/"
__version__ = "0.0.1"
__maintainer__ = "David C. Petty"
__email__ = "dpetty@winchsterps.org"
__status__ = "Hack"


class TOY:
    """Simulator and assembler for the Princeton COS 126 TOY computer."""

    def __init__(self):
        """Initialize a Toy program."""
        # Symbolic constants
        self._register = {
            'R[0]': 0x0, 'R[1]': 0x1, 'R[2]': 0x2, 'R[3]': 0x3,
            'R[4]': 0x4, 'R[5]': 0x5, 'R[5]': 0x6, 'R[7]': 0x7,
            'R[8]': 0x8, 'R[9]': 0x9, 'R[A]': 0xA, 'R[B]': 0xB,
            'R[C]': 0xC, 'R[D]': 0xD, 'R[E]': 0xE, 'R[F]': 0xF, }
        self._operation = {
            '+': 1, '-': 2, '&': 3, '^': 4, '<<': 5, '>>': 6, }
        self._memory = ['M[', ]
        self._noop = ['<-', ']', ]
        self._jump = {
            'BRANCH=0': 0xC, 'BRANCH>0': 0xD, 'JUMP': 0xE, 'LINK': 0xF, }
        self._branch = [
            'IF<>0', 'IF<=0', 'ELSE', 'THEN', 'WHILE<>0', 'WHILE<=0', 'REPEAT',
        ]
        self._init()

    def _init(self):
        """Initialize assembly variables."""
        self.memory = [0, ] * 256                   # TOY memory
        self.registers = [0, ] * 16                 # TOY registers
        self.code = ''                              # TOY code listing
        self._statements = [[] for _ in range(256)]  # list of statement lists
        self._labels = {}                           # dict of labels
        self._control = []                          # control structure stack

    # ///////////////////////////// SIMULATOR //////////////////////////////

    # // http://www.cs.princeton.edu/courses/archive/spring17/cos126/lectures/CS.18.MachineII.pdf
    # public class TOYlecture
    # {
    #    // TOY simulator
    #    public static void main(String[] args)
    #    {
    #        int pc = 0x10; // program counter
    #        int[] R = new int[16]; // registers
    #        int[] M = new int[256]; // main memory
    #        In in = new In(args[0]);
    #        for (int i = 0x10; i < 0xFF && !in.isEmpty(); i++)
    #            M[i] = Integer.parseInt(in.readString(), 16);
    #        while (true)
    #            int op = (ir >> 12) & 0xF; // opcode (bits 12-15)
    #            int d = (ir >> 8) & 0xF; // dest d (bits 08-11)
    #            int s = (ir >> 4) & 0xF; // source s (bits 04-07)
    #            int t = (ir >> 0) & 0xF; // source t (bits 00-03)
    #            int addr = (ir >> 0) & 0xFF; // addr (bits 00-07)
    #            if (op == 0) break; // halt
    #            switch (op)
    #            {
    #                case 1: R[d] = R[s] + R[t]; break;
    #                case 2: R[d] = R[s] - R[t]; break;
    #                case 3: R[d] = R[s] & R[t]; break;
    #                case 4: R[d] = R[s] ^ R[t]; break;
    #                case 5: R[d] = R[s] << R[t]; break;
    #                case 6: R[d] = R[s] >> R[t]; break;
    #                case 7: R[d] = addr; break;
    #                case 8: R[d] = M[addr]; break;
    #                case 9: M[addr] = R[d]; break;
    #                case 10: R[d] = M[R[t]]; break;
    #                case 11: M[R[t]] = R[d]; break;
    #                case 12: if (R[d] == 0) pc = addr; break;
    #                case 13: if (R[d] > 0) pc = addr; break;
    #                case 14: pc = R[d]; break;
    #                case 15: R[d] = pc; pc = addr; break;
    #            }
    #        }
    #    }
    # }

    def _output(self, value, bits=16):
        """Output hex and 16-bit 2's-complement value."""
        # https://stackoverflow.com/a/32031543/17467335
        sgn = 1 << (bits - 1)
        print("0x{:04X} = {}".format(value, (value & (sgn - 1)) - (value & sgn)))

    # Toy simulator (after COS 126 'Toy simulator in Java' from Lecture 18).
    def _store(self, M, addr, value):
        """Store value at M[ addr ] and handle memory-mapped output at 0xFF."""
        M[addr] = value
        if addr == 0xFF:
            self._output(value)

    def _load(self, M, addr):
        """Return value at M[ addr ] and handle memory-mapped input at 0xFF."""
        if addr == 0xFF:
            M[addr] = int(input('input? '))
        return M[addr]

    def run(self, pc=0x10):
        """Run program in memory starting at pc."""
        M, R, PC = self.memory, self.registers, pc
        while(True):
            ir = M[PC]
            PC += 1
            op = (ir >> 12) & 0xF   # opcode (bits 12-15)
            d = (ir >> 8) & 0xF     # dest d (bits 08-11)
            s = (ir >> 4) & 0xF     # source s (bits 04-07)
            t = (ir >> 0) & 0xF     # source t (bits 00-03)
            addr = (ir >> 0) & 0xFF  # addr (bits 00-07)
            if (op == 0):
                break   # halt
            elif op == 1:
                R[d] = R[s] + R[t]
            elif op == 2:
                R[d] = R[s] - R[t]
            elif op == 3:
                R[d] = R[s] & R[t]
            elif op == 4:
                R[d] = R[s] ^ R[t]
            elif op == 5:
                R[d] = R[s] << R[t]
            elif op == 6:
                R[d] = R[s] >> R[t]
            elif op == 7:
                R[d] = addr
            elif op == 8:
                # R[d] = M[addr]
                R[d] = self._load(M, addr)
            elif op == 9:
                # M[addr] = R[d]
                self._store(M, addr, R[d])
            elif op == 10:
                # R[d] = M[R[t]]
                R[d] = self._load(M, R[t])
            elif op == 11:
                # M[R[t]] = R[d]
                self._store(M, addr, R[t])
            elif op == 12:
                if (R[d] == 0):
                    PC = addr
            elif op == 13:
                if (R[d] > 0):
                    PC = addr
            elif op == 14:
                PC = R[d]
            elif op == 15:
                R[d] = PC
                PC = addr

    # ///////////////////////////// ASSEMBLER //////////////////////////////

    def _isNumber(self, op):
        """Return True if op is (signed) hexadecimal, otherwise False."""
        return bool(re.match('[-+0-9A-F]+$', op))

    def _isLabel(self, op):
        """Return True if op not a register symbol, otherwise False."""
        return op not in self._register

    def _isHalt(self, ops):
        """HALT"""
        return len(ops) == 1 and ops[0] == 'HALT'

    def _isOperation(self, ops):
        """R[A] <- R[B] + R[C]
        R[A] <- R[B] - R[C]
        R[A] <- R[B] & R[C]
        R[A] <- R[B] ^ R[C]
        R[A] <- R[B] << R[C]
        R[A] <- R[B] >> R[C]"""
        return (len(ops) == 5 and
                all(ops[i] in self._register for i in [0, 2, 4, ]) and
                ops[3] in self._operation)

    def _isMove(self, ops):
        """R[A] <- R[B]"""
        return (len(ops) == 3 and
                all(ops[i] in self._register for i in [0, 2, ]))

    def _isLoadAddress(self, ops):
        """R[A] < - LABEL"""
        return (len(ops) == 3 and
                ops[0] in self._register and
                (self._isNumber(ops[2]) or self._isLabel(ops[2])))

    def _isLoad(self, ops):
        """R[A] <- M[ LABEL ]"""
        return (len(ops) == 5 and
                ops[0] in self._register and
                ops[2] in self._memory and
                (self._isNumber(ops[3]) or self._isLabel(ops[3])))

    def _isStore(self, ops):
        """M[ LABEL ] <- R[A]"""
        return (len(ops) == 5 and
                ops[0] in self._memory and
                (self._isNumber(ops[1]) or self._isLabel(ops[1])) and
                ops[4] in self._register)

    def _isRead(self, ops):
        """READ R[A]"""
        return (len(ops) == 2 and
                ops[0] == 'READ' and ops[1] in self._register)

    def _isWrite(self, ops):
        """WRITE R[A]"""
        return (len(ops) == 2 and
                ops[0] == 'WRITE' and ops[1] in self._register)

    def _isLoadIndirect(self, ops):
        """R[A] <- M[ R[B] ]"""
        return (len(ops) == 5 and
                ops[0] in self._register and
                ops[2] in self._memory and ops[3] in self._register)

    def _isStoreIndirect(self, ops):
        """M[ R[A] ] <- R[B]"""
        return (len(ops) == 5 and
                ops[0] in self._memory and
                ops[1] in self._register and ops[4] in self._register)

    def _isJump(self, ops):
        """JUMP R[A]"""
        return (len(ops) == 2 and
                ops[0] in self._jump and ops[1] in self._register)

    def _isJumpLink(self, ops):
        """BRANCH=0 R[A] LABEL
        BRANCH>0 R[A] LABEL
        LINK R[A] LABEL"""
        return (len(ops) == 3 and
                ops[0] in self._jump and ops[1] in self._register and
                self._isLabel(ops[2]))

    def _isGoto(self, ops):
        """GOTO LABEL"""
        return (len(ops) == 2 and
                ops[0] == 'GOTO' and self._isLabel(ops[1]))

    def _isLabelRelative(self, ops):
        """: LABEL"""
        return len(ops) == 2 and ops[0] == ':'

    def _isLabelAbsolute(self, ops):
        """: LABEL 12"""
        return (len(ops) == 3 and
                ops[0] == ':' and   # RED_FLAG: requires a number
                self._isNumber(ops[2]))

    def _isStoreLabel(self, ops):
        """! LABEL 1234"""
        return (len(ops) == 3 and
                ops[0] == '!' and   # RED_FLAG: requires a number
                self._isLabel(ops[1]) and self._isNumber(ops[2]))

    def _isAllocate(self, ops):
        """. 1234"""
        return (len(ops) == 2 and
                ops[0] == '.' and   # RED_FLAG: requires a number
                self._isNumber(ops[1]))

    def _isAllocateLabel(self, ops):
        """. LABEL 1234"""
        return (len(ops) == 3 and
                ops[0] == '.' and   # RED_FLAG: requires a number
                self._isLabel(ops[1]) and self._isNumber(ops[2]))

    def _isIfWhileNotEqual(self, ops):
        """IF<>0 R[A]
        WHILE<>0 R[A]"""
        return (len(ops) == 2 and
                ops[0] in ['IF<>0', 'WHILE<>0', ] and
                ops[1] in self._register)

    def _isIfWhileLessThan(self, ops):
        """IF<=0 R[A]
        WHILE<=0 R[A]"""
        return (len(ops) == 2 and
                ops[0] in ['IF<=0', 'WHILE<=0', ] and
                ops[1] in self._register)

    def _isWord(self, ops, word):
        """WORD"""
        return (len(ops) == 1 and ops[0] == word)

    def _address(self, op):
        """Return op if number, value if defined label, or add forward
        reference and return zero."""
        if self._isNumber(op):
            value = int(op, 16)
            assert value == value & 0xFF
            return int(op, 16)
        if op in self._labels and isinstance(self._labels[op], int):
            return self._labels[op]
        if op not in self._labels:
            self._labels[op] = []
        self._labels[op].append(self._labels['PC'])
        return 0x00

    def _patch(self, label, value):
        """Return value, after update label and resolve forward references."""
        assert value == value & 0xFF
        if label in self._labels and isinstance(self._labels[label], list):
            for addr in self._labels[label]:
                self.memory[addr] = self.memory[addr] & 0xFF00 | value
        self._labels[label] = value
        return value

    def _increment(self):
        """Increment PC."""
        self._labels['PC'] += 1

    def _saveStatement(self, address, line):
        """Save statement line at address."""
        self._statements[address].append(line.rstrip())

    def _assemble(self, op, line):
        """Assemble op into memory, _increment PC, and save statment line."""
        pc = self._labels['PC']
        self.memory[pc] = op
        self._saveStatement(pc, line)
        self._increment()

    # http://introcs.cs.princeton.edu/java/60machine/reference.txt
    # http://introcs.cs.princeton.edu/java/62toy/
    def asm(self, program, pc=0x10):
        """Assemble program (str or list) into memory at pc."""
        self._init()
        self._labels['PC'] = pc
        # Process lines of program.
        lines = program.splitlines() if isinstance(program, str) else program
        for line in lines:
            # Parse lines on spaces and remove comments on #.
            code = line.split('#')[0].strip()
            ops = [op.upper() for op in code.split(' ')]
            # Check each type of instruction.
            # HALT
            if self._isHalt(ops):
                op = 0
                self._assemble(op * 4096, line)
            # R[A] <- R[B] + R[C]
            # R[A] <- R[B] - R[C]
            # R[A] <- R[B] & R[C]
            # R[A] <- R[B] ^ R[C]
            # R[A] <- R[B] << R[C]
            # R[A] <- R[B] >> R[C]
            elif self._isOperation(ops):
                rD, arrow, rS, op, rT = (self._register[ops[0]], ops[1],
                                         self._register[ops[2]],
                                         self._operation[ops[3]],
                                         self._register[ops[4]])
                self._assemble(op * 4096 + rD * 256 + rS * 16 + rT * 1, line)
            # R[A] <- R[B]
            elif self._isMove(ops):
                op, rD, arrow, rS = (1, self._register[ops[0]], ops[1],
                                     self._register[ops[2]])
                self._assemble(op * 4096 + rD * 256 + rS * 16, line)
            # R[A] <- LABEL
            elif self._isLoadAddress(ops):
                op, rD, arrow, addr = (7, self._register[ops[0]],
                                       ops[1], self._address(ops[2]))
                self._assemble(op * 4096 + rD * 256 + addr * 1, line)
            # R[A] <- M[ LABEL ]
            elif self._isLoad(ops):
                op, rD, arrow, mem, addr, bracket = (8, self._register[ops[0]],
                                                     ops[1], ops[2],
                                                     self._address(ops[3]),
                                                     ops[4])
                self._assemble(op * 4096 + rD * 256 + addr * 1, line)
            # M[ LABEL ] <- R[A]
            elif self._isStore(ops):
                op, mem, addr, bracket, arrow, rD = (9, ops[0],
                                                     self._address(ops[1]),
                                                     ops[2], ops[3],
                                                     self._register[ops[4]])
                self._assemble(op * 4096 + rD * 256 + addr * 1, line)
            # READ R[A]
            elif self._isRead(ops):
                op, name, rD, addr = 8, ops[0], self._register[ops[1]], 0xFF
                self._assemble(op * 4096 + rD * 256 + addr * 1, line)
            # WRITE R[A]
            elif self._isWrite(ops):
                op, name, rD, addr = 9, ops[0], self._register[ops[1]], 0xFF
                self._assemble(op * 4096 + rD * 256 + addr * 1, line)
            # R[A] <- M[ R[B] ]
            elif self._isLoadIndirect(ops):
                op, rD, arrow, mem, rT, bracket = (0xA, self._register[ops[0]],
                                                   ops[1], ops[2],
                                                   self._register[ops[3]],
                                                   ops[4])
                self._assemble(op * 4096 + rD * 256 + rT * 1, line)
            # M[ R[A] ] <- R[B]
            elif self._isStoreIndirect(ops):
                op, mem, rT, bracket, arrow, rD = (0xB, ops[0],
                                                   self._register[ops[1]],
                                                   ops[2], ops[3],
                                                   self._register[ops[4]])
                self._assemble(op * 4096 + rD * 256 + rT * 1, line)
            # JUMP R[A]
            elif self._isJump(ops):
                op, jump, rD = 0xE, ops[0], self._register[ops[1]]
                self._assemble(op * 4096 + rD * 256, line)
            # BRANCH=0 R[A] LABEL
            # BRANCH>0 R[A] LABEL
            # LINK R[A] LABEL
            elif self._isJumpLink(ops):
                jump, rD, addr = (ops[0], self._register[ops[1]],
                                  self._address(ops[2]))
                op = self._jump[jump]
                self._assemble(op * 4096 + rD * 256 + addr * 1, line)
            # GOTO LABEL
            elif self._isGoto(ops):
                op, rD, addr = (0xC, self._register['R[0]'],
                                self._address(ops[1]))
                self._assemble(op * 4096 + rD * 256 + addr, line)
            # IF<>0 R[A]
            # WHILE<>0 R[A]
            elif self._isIfWhileNotEqual(ops):
                op, rD = 0xC, self._register[ops[1]]
                self._control.append(self._labels['PC'])
                self._assemble(op * 4096 + rD * 256, line)
            # IF<=0 R[A]
            # WHILE<=0 R[A]
            elif self._isIfWhileLessThan(ops):
                op, rD = 0xD, self._register[ops[1]]
                self._control.append(self._labels['PC'])
                self._assemble(op * 4096 + rD * 256, line)
            # ELSE
            elif self._isWord(ops, 'ELSE'):
                branch, here = self._control.pop(), self._labels['PC']
                op, rD = 0xC, self._register['R[0]']
                self._control.append(here)
                self._assemble(op * 4096 + rD * 256, line)
                self.memory[branch] = self.memory[branch] + here + 1
            # THEN
            elif self._isWord(ops, 'THEN'):
                branch, here = self._control.pop(), self._labels['PC']
                self.memory[branch] = self.memory[branch] + here
                self._saveStatement(here, line)
            # REPEAT
            elif self._isWord(ops, 'REPEAT'):
                branch, here = self._control.pop(), self._labels['PC']
                op, rD = 0xC, self._register['R[0]']
                self._assemble(op * 4096 + rD * 256 + branch, line)
                self.memory[branch] = self.memory[branch] + here + 1
            # : LABEL
            elif self._isLabelRelative(ops):
                colon, label, pc = ops[0], ops[1], self._labels['PC']
                self._patch(label, pc)
                self._saveStatement(self._labels['PC'], line)
            # : LABEL 12
            elif self._isLabelAbsolute(ops):
                colon, label, value = ops[0], ops[1], int(ops[2], 16)
                self._patch(label, value)
                self._saveStatement(self._labels['PC'], line)
            # ! LABEL 1234
            elif self._isStoreLabel(ops):
                bang, label, value = ops[0], ops[1], int(ops[2], 16) & 0xFFFF
                assert label in self._labels, '! missing label: ' + label
                self.memory[self._labels[label]] = value
                self._saveStatement(self._labels[label], line)
            # . 1234
            elif self._isAllocate(ops):
                dot, value, pc = (ops[0], int(ops[1], 16) & 0xFFFF,
                                  self._labels['PC'])
                self.memory[pc] = value
                self._saveStatement(pc, line)
                self._increment()
            # . LABEL 1234
            elif self._isAllocateLabel(ops):
                dot, label, value, pc = (ops[0], ops[1],
                                         int(ops[2], 16) & 0xFFFF,
                                         self._labels['PC'])
                self.memory[self._patch(label, pc)] = value
                self._saveStatement(pc, line)
                self._increment()
            # # COMMENT
            elif line:
                if not re.match('\s*#', line):
                    line = '# {}'.format(line)
                self._saveStatement(self._labels['PC'], line)
        # Make sure all labels are defined.
        for label in self._labels:
            assert not isinstance(self._labels[label], list), \
                'undefined label: ' + label
        # Make sure all control structures are balanced.
        assert len(self._control) == 0, 'control structures not balanced'

    def listing(self, filename=None):
        """Save listing of compiled program in filename (or print if None)."""
        self.code = ''
        for i in range(256):
            if self.memory[i] or self._statements[i]:
                for statement in self._statements[i]:
                    if statement is not None:
                        self.code += '{}{}\n'.format(' ' * 11, statement)
                self.code += '{:02X}: {:04X}\n'.format(i, self.memory[i])
        # Write or print self.code.
        if filename:
            with open(filename, 'w') as outFile:
                outFile.write(self.code)
        else:
            print(self.code)
