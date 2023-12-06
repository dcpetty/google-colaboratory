#################################################################
#
# Test of random other code...
#
NOT A VALID STATEMENT, SO IT IS A COMMENT
: start                             # can be upper / lower case
R[1] <- 1
IF<>0 R[D]
    M[ COUNT ] <- R[D]  # test
    R[D] <- M[ R[D] ]   # test
    M[ R[D] ] <- R[D]   # test
    R[D] <- M[ COUNT ]  # test
    R[2] NOOP_TOKENS M[ COUNT ARE_NOT_CHECKED   # test
ELSE
    R[A] <- R[B] + R[C]
    R[A] <- R[B] - R[C]
    R[A] <- R[B] & R[C]
    R[A] <- R[B] ^ R[C]
    R[A] <- R[B] << R[C]
    R[A] <- R[B] >> R[C]
    BRANCH=0 R[D] START
    BRANCH>0 R[D] END
    JUMP R[D]
    LINK R[D] START
    R[E] <- M[ R[F] ]
    M[ R[E] ] <- R[F]
    WHILE<>0 R[E]
        R[E] <- R[E] - R[1]
    REPEAT
THEN
: END
GOTO START
. 1234
. COUNT 5678
. THIS abcd                         # Where is this comment
: THAT                              # Where is that comment
! THAT -3F22                        # And this?
