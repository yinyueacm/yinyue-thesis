#include "ropeman.h"
#include "scoreboard.h"
#include "display.h"
#include "config.h"

char flag_id[32];
char f_status[255];

User curUser = {
    .userId = {0},
    .userPasswd = {0},
    .score = {0},
    .status = {0},
};

char guesswords[700][50];
int current_topic = -1;
int current_size = 0;

int checkASLR();

char* getInitScore() {
    srand(time(NULL));
    char *randScore = calloc(sizeof(char), 17);
    sprintf(randScore, "%d", rand()%100);
    debug("generated score is %s\n", randScore);

    return randScore;
}

void removeChar(char *str, char garbage) {

    char *src, *dst;
    for (src = dst = str; *src != '\0'; src++) {
        *dst = *src;
        if (*dst != garbage) dst++;
    }
    *dst = '\0';
}

int getGuesslist(char* category){
    char* filepath = malloc(100 * sizeof(char));
    FILE * fp;
    size_t len = 50;
    char* line = malloc(len * sizeof(char));
    int i = 0;

    sprintf(filepath, "%s%s.txt", WLHOME, category);
    fp = fopen(filepath, "r");

    if(fp == NULL){
        //exception handling
        debug("getguesslist wrong\n");
        return -1;
    }
    while(fgets(line, len, fp) != NULL){
        debug("%s\n", line);
        removeChar(line, '\n');
        strncpy(guesswords[i], line, 50);
        i++;
    }
    free(filepath);
    free(line);
    fclose(fp);

    return i;
}
/*
Function: getGuessWord
Description: Randomly choose a word in guessWords[] as the key-word
! guesswords should be filled first
*/
int getGuessWord(int size, char **theWord){
    //pick up a random number
    srand(time(NULL));
    int randIdx = 0;

    // disgard words longer than 27 because of display size
    while(strlen(guesswords[randIdx = rand() % size]) >= 27);

    *theWord = guesswords[randIdx];

    debug("[%s]\n", *theWord);

    return strlen(*theWord);
}

void getStr(char * buf, int inputLen, FILE* fd) {
    int c, i=0;
    setbuf(stdin, NULL);
    while((c=fgetc(stdin))!='\n' && c != EOF && i < inputLen){
        buf[i++] = c;
    }
}

int getChar(FILE* fd) {
    int c = 0, ign = 0;
    setbuf(stdin, NULL);
    c = fgetc(stdin);
    while (ign != '\n' && ign != EOF){
        ign = fgetc(stdin);
    }
    return c;
}

void getInput() {
    char *userId, *userPasswd;

    userId = calloc(sizeof(char), INPUTMAX);
    userPasswd = calloc(sizeof(char), INPUTMAX);

    output("Please input your user id\n:  ");
    getStr(userId, INPUTMAX, stdin);

    output("Please input your password\n:  ");
    getStr(userPasswd, INPUTMAX, stdin);

    memcpy(curUser.userId, userId, sizeof(curUser.userId)-1);
    memcpy(curUser.userPasswd, userPasswd, sizeof(curUser.userPasswd)-1);

    free(userId);
    free(userPasswd);
}

int selectLevel1() {
    int c               = 0;
    int rtnCode         = RTN_LEVEL1;

    while (rtnCode == RTN_LEVEL1) {
        printLevel1();
        c = getChar(stdin);
        switch (c) {
            case 'C':                     // create new user
            case 'c':
                getInput();                 // get user id and password
                char *score = getInitScore();
                debug("generated score is %s\n", score);
                memcpy(curUser.score, score, strlen(score));
                int nfret = new_file();
                if (nfret < 0 ){
                    output("Create User Error! Please check your input\n:  ");                 break;   
                }
                rtnCode = RTN_LEVEL2;
                break;
            case 'L':                     // login with exsiting id
            case 'l':
                getInput();                 // get user_id and password
                char * content = calloc(sizeof(char), 64);
                User u = {
                    .userId = {0},
                    .userPasswd = {0},
                    .score = {0},
                    .status = {0},
                };
                content = read_file(curUser.userId);
                if(strcmp(content, "[***OPENFILEWRONG***]") == 0){
                    output("Wrong User ID! Please check your input\n:  ");
                    break;
                }
                get_content(content, &u);
                debug("User input passwd for [%s]: [%s]\n",curUser.userId, curUser.userPasswd);
                debug("Stored passwd for [%s]: [%s][%s]\n",curUser.userId, u.userPasswd, u.score);
                if (strcmp(curUser.userPasswd, u.userPasswd) == 0 ) {
                    memcpy(curUser.score, u.score, sizeof(curUser.score)-1);
                    memcpy(curUser.status, u.status, sizeof(curUser.status)-1);
                    memcpy(flag_id, u.status, sizeof(flag_id)-1);
                    rtnCode = RTN_LEVEL2;
                }
                break;
            case 'X':                     // quit
            case 'x':
                rtnCode = RTN_EXIT;
            case 'S':                     // show scoreboard
            case 's':
                printScoreboard();
                break;
            default:
                output("Please enter a valid command!(C | L | S | X)\n:  ");
                break;
        }
    }
    return rtnCode;
}

void updateStatus()
{
    printLine();
    output("Be creative with your status, put any crap you want here:");
    output("  (but in less than 128 characters) \n:  ");
    char *status = calloc(sizeof(char), 128+1);
    getStr(status, 128, stdin);

    memcpy(curUser.status, status, 128);
    memcpy(flag_id, status, sizeof(flag_id)-1);
    write_file();

}

int selectContinue() {
    char sSelection[BUF_SIZE]   = {0};
    int rtnCode                 = RTN_LOOP;

    while (rtnCode == RTN_LOOP) {
        printContinue();
        //scanf("%s", sSelection);
        getStr(sSelection, MAX_SIZE, stdin);
        switch (sSelection[0]) {
            case 'S':
            case 's':
                rtnCode = RTN_LEVEL4;
                break;
            case 'Q':                     // continue by choosing another category
            case 'q':
                rtnCode = RTN_LEVEL3;
                break;
            case 'X':                     // quit
            case 'x':
                printScoreboard();
                rtnCode = RTN_EXIT;
                break;
            default:
                output("Please enter a valid command!(S | Q | X)\n:  ");
                break;
        }
    }

    return rtnCode;
}

int selectLevel2() {
    int c               = 0;
    int rtnCode         = RTN_LEVEL2;

    while (rtnCode == RTN_LEVEL2) {
        printLevel2();
        c = getChar(stdin);
        switch (c) {
            case 'C':                     // continue by choosing category
            case 'c':
                rtnCode = RTN_LEVEL3;
                break;
            case 'M':                     // continue by choosing category
            case 'm':
                updateStatus();
                break;
            case 'Q':                     // quit
            case 'q':
                rtnCode = RTN_LEVEL1;
                break;
            case 'X':                     // quit
            case 'x':
                rtnCode = RTN_EXIT;
            case 'S':                     // show scoreboard
            case 's':
                // show scoreboard
                printScoreboard();
                break;
            default:
                output("Please enter a valid command!(C | S | Q | M | Z))\n:  ");
                break;
        }
    }
    return rtnCode;
}

int selectCategory(int * nCategory) {
    printCategory((char **) wordlists);
    int c = 0;
    int rtnCode = RTN_LEVEL4;
    while ((c = getChar(stdin))) {
        if(c == 'Q' || c == 'q' ) {
            rtnCode = RTN_LEVEL2;
            break;
        } else if(c == 'X' || c == 'x' ) {
            rtnCode = RTN_EXIT;
            break;
        } else if(c >= '0' && c <= '7') {
            *nCategory = c;
            break;
        } else{
            output("Please make a valid selection\n:  ");
        }
    }
    return rtnCode;
}

int playRopeman(int topic) {

    int rtnCode            = 0;
    int failed             = 0;

    GuessState curState = {
        .flag = 0,
        .nEntered = 0,
        .nGuessed = 0,
        .nFailed = 0,
        .letterEntered = 0,
        .lettersEntered = {0},
        .lettersFound = {0},
        .theWord = calloc(sizeof(char), MAXWORDLEN),
    };

    if (topic != current_topic){
        debug("Changing topic\n");
        int size = getGuesslist(wordlists[topic]);
        if (size == -1){
            debug("read file wrong\n");
            return RTN_ERROR;
        }
        current_topic = topic;
        current_size = size;
    }

    curState.lenWord = getGuessWord(current_size, &(curState.theWord));
    while(curState.nGuessed < curState.lenWord && curState.nFailed < LEVEL_HARD){
        printState(curState);
        curState.letterEntered = getChar(stdin);
        curState.nEntered ++;

        if((curState.letterEntered >= 'A') &&
                (curState.letterEntered <= 'Z')){
            curState.letterEntered = curState.letterEntered - 'A' + 'a';
        }

        if((curState.letterEntered >= 'a') &&
                (curState.letterEntered <= 'z')){
            curState.lettersEntered[curState.letterEntered - 'a'] = 1;
        }else if(curState.letterEntered == ' '){
            curState.lettersEntered[26] = 1;
        }else{
            debug("Illegal input!\n");
            continue;
        }

        int i = 0;
        int found = 0;
        for (i = 0; i < curState.lenWord; i++){
            if( (curState.letterEntered == curState.theWord[i]) && (curState.lettersFound[i] == 0)){
                found = 1;
                curState.lettersFound[i] = 1;
                curState.nGuessed ++;
            }
        }
        if(found == 0){
            if (++curState.nFailed == LEVEL_HARD){
                failed = 1;
                break;
            }
        }
    }

    printState(curState);

    if(failed == 1){
        output("Sorry you missed it. The word is [%s]\n", curState.theWord);
    } else{
        output("Good job! You made it!\n");
        long previsouScore = strtol(curUser.score, NULL, 10);
        sprintf(curUser.score, "%16ld", previsouScore + curState.lenWord + LEVEL_HARD - curState.nFailed);
        write_file();
    }
    rtnCode = selectContinue();

    return rtnCode;
}

int main(int argc, char* argv[]){
#ifdef CHECK
    checkASLR();
#endif
    debug("%lx\n", (unsigned long)&flag_id);
    debug("%lx\n", (unsigned long)&f_status);
    debug("%lx\n", (unsigned long)&read_file);
    debug("%lx\n", (unsigned long)&output);
    //selectContinue();
    int rtn = RTN_LEVEL1;
    int nCategory = 0;
    printWelcome();

    while(1) {
        if(rtn == RTN_LEVEL1) {
            rtn = selectLevel1();
        }
        if (rtn == RTN_LEVEL2) {
            rtn = selectLevel2();
        }
        if (rtn == RTN_LEVEL3) {
            rtn = selectCategory( &nCategory );
        }
        if (rtn == RTN_LEVEL4) {
            rtn = playRopeman(nCategory-'0');
        }
        if(rtn == RTN_EXIT) {
            break;
        }
        if(rtn == RTN_ERROR) {
            break;
        }
    }
    return 0;
}

