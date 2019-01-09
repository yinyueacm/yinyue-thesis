#ifndef _HANGMAN_H
#define _HANGMAN_H

#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
#include <dirent.h>
#include <stdint.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <err.h>
#include <errno.h>
#include "scoreboard.h"
#include "display.h"

#define LEVEL_EASY      8
#define LEVEL_MEDIUM    6
#define LEVEL_HARD      6

// indicates a "continue" in the outermost while loop
#define RTN_LOOP        100001
#define RTN_LEVEL1      100003
#define RTN_LEVEL2      100004
#define RTN_LEVEL3      100005
#define RTN_LEVEL4      100006
#define RTN_EXIT        100002      //exit and lose share same code
#define RTN_ERROR       -1

#define INPUTMAX        32
#define MAXWORDLEN      50

#define FLAGFILENAME    "CatchMeIfYouCan"

#ifndef SERVICEHOME
#define SERVICEHOME     "../"
#endif
#define RWHOME          SERVICEHOME  "rw/"
#define ROHOME          SERVICEHOME  "ro/"
#define WLHOME          ROHOME  "wordlists/"

#define BUF_SIZE        20
#define MAX_SIZE        60

#ifdef DEBUG
#define debug(M, ...) fprintf(stderr, "DEBUG %s:%d: " M "\n", __FILE__, __LINE__, ##__VA_ARGS__)
#else
#define debug(M, ...)
#endif

static char * const wordlists[] = {
    "animals",
    "fruits",
    "instruments",
    "passwords",
    "programming-languages",
    "science",
    "sports",
    "stack-exchange-sites",
    NULL
};


#endif

