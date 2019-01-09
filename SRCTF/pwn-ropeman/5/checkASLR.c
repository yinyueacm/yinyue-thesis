#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int global = 0;

int checkASLR() {

    int     stack = 0;
    char    *heap = malloc(1);

    printf ("\n# ========================\n"
            "#  Time:   %d\n"
            "# ========================\n"
            "#  _TEXT_: %p\n"
            "#  Global: %p\n"
            "#  Stack:  %p\n"
            "#  Heap:   %p\n"
            "# ========================\n",
            (int)time(NULL),
            checkASLR,
            &global,
            &stack,
            heap);

    return 0;
}

