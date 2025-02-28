#################################################################
#
# Fibonacci program, loaded at location 0x40
#
GOTO START              # TOY simulator requires instruction at 0x10
: PC 40
: START
R[1] <- 01              # R1 <- decrement
R[9] <- M[ COUNT ]      # R9 <- COUNT (forward reference)
R[A] <- 00              # RA <- previous Fibonacci number
R[B] <- 01              # RB <- current Fibonacci number
WHILE<>0 R[9]
    R[C] <- R[A] + R[B] # calculate next Fibonacci number
    R[A] <- R[B]        # shift previous Fibonacci number
    R[B] <- R[C]        # shift current Fibonacci number
    WRITE R[B]          # send current Fibonacci number to stdout
    R[9] <- R[9] - R[1] # decrement counter
REPEAT
: STOP
HALT                    # the HALT statement
. COUNT 0017
