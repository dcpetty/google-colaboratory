#################################################################
#
# Fibonacci program, loaded at location 0x40
#
GOTO START          # TOY simulator requires an instruction at 0x10
: PC 40
: START
R[1] <- 01
R[9] <- M[ COUNT ]  # forward reference to COUNT
R[A] <- 01
R[B] <- 01
WHILE<>0 R[9]
    WRITE R[A]
    R[C] <- R[A] + R[B]
    R[A] <- R[B]
    R[B] <- R[C]
    R[9] <- R[9] - R[1]
REPEAT
: STOP              # the HALT statement
HALT
. COUNT 0017
