#include "ropeman.h"
#include <stdarg.h>

void output(const char *fmt, ...) {
    debug("[you are in output] You have got here\n");
    va_list args;
    va_start(args, fmt);
    printf("{");
    vprintf(fmt, args);
    va_end(args);
    printf("}\n");
    fflush(stdout);
}

void printLevel1() {
    printShortLine();
    printf("C.) Create new user\n");
    printf("L.) Log in with existing account\n");
    printf("S.) Show the score\n");
    printf("X.) Exit\n");
    printShortLine();
    printf(":  ");
    fflush(stdout);
}

void printScore() {
    extern User curUser;
    printLine();
    printf("Hi [%s], your current score is [%s]\n", curUser.userId, curUser.score);
    printf("Your status: [%s]\n", curUser.status);
    printf("what would you like to do next?\n");
    fflush(stdout);
}

void printLevel2() {
    printScore();
    printShortLine();
    printf("C.) Choose a category to play\n");
    printf("S.) Show the scoreboard\n");
    printf("M.) Modify your status\n");
    printf("Q.) Go back to the previous menu\n");
    printf("X.) Exit\n");
    printShortLine();
    printf(":  ");
    fflush(stdout);
}

void printContinue() {
    printScore();
    printShortLine();
    printf("S.) Start another game in this category\n");
    printf("Q.) Go back to the previous menu\n");
    printf("X.) Exit\n");
    printShortLine();
    printf(":  ");
    fflush(stdout);
}

void printContinue2() {
    printShortLine();
    printf("S.) Start another game in this category\n");
    printf("X.) Exit\n");
    printShortLine();
    printf(":  ");
    fflush(stdout);
}

void printCategory(char **list) {
    printLine();
    printf("please select a category:\n");
    printShortLine();
    int i = 0;
    for(; list[i] != NULL; i++) {
        printf("%d.) %s \n", i , list[i]);
    }
    printf("Q.) Go back to the previous menu\n");
    printf("X.) Exit\n");
    printShortLine();
    printf(":  ");
    fflush(stdout);
}

void printScoreboard() {
    printLine();
    Ranking* rk = calloc(sizeof(Ranking), 12);
    int i = 0;
    int nRecords = sort_score(rk);
    printf("+------------+----------------------------------+-------------------+\n");
    printf("|    RANK    |              User ID             |        SCORE      |\n");
    printf("+------------+----------------------------------+-------------------+\n");

    /*printf("| %7d    |%32s\t|%16s   |\n", rk->rk, rk->user.userId, "SECRET!");*/
    for(i = 0; i < nRecords; i++) {
       printf("| %7d    |%32s\t|%16s   |\n", rk->rk, rk->user.userId, rk->user.score);
       rk++;
    }
    printf("+------------+----------------------------------+-------------------+\n");
    fflush(stdout);
}

void printLine() {
    printf("%s\n", DELIMITER);
    fflush(stdout);
}

void printShortLine() {
    printf("%s\n", SHORTDELIMITER);
    fflush(stdout);
}
void printWelcome() {
    int i = 0;
    printLine();
    for(i = 0; i < LOGOHEIGHT; i++) {
        printf("%s\n", welcome[i]);
    }
    printLine();
    printf("Welcome to our carelessly built ROPEman game at drunk time.\n");
    printf("Our goal is to provide robust software as strong as Flash \n");
    printf("In order to thank you for your support on our alpha testing\n");
    printf("Every newly registered user will get a \"welcome score\"\n");
    printf("Please select one action:\n");
    fflush(stdout);
}

void printGallows(int state) {
    printLine();
    int i = 0;
    for ( i = 0; i < GALLOWSHEIGHT; i++) {
        printf("%s\n", gallows[state][i]);
    }
    printLine();
    fflush(stdout);
}

void printState(GuessState state) {
    char * displayWord;
    char sPlaceholder[64] = {0};
    char screen[23][92] = { {0} };
    int i = 0;

    printLine();
    // start populating the screen
    for(i = 0; i < 23; i++) {
        memcpy(&screen[i], frame[i], sizeof(screen[0])-1);
    }

    // the word - 54 spaces
    displayWord = malloc(2 * state.lenWord * sizeof(char));
    for ( i = 0; i < state.lenWord; i++) {
        if(state.lettersFound[i] == 0) {
            sprintf(displayWord + 2*i ,"_ ");
        }else if(state.lettersFound[i] == 1) {
            sprintf(displayWord + 2*i,"%c ", state.theWord[i]);
        }
    }

    int offset = 27 - state.lenWord + 3;
    sprintf(sPlaceholder, "[%s]", displayWord);
    memcpy(screen[6] + offset, sPlaceholder, strlen(sPlaceholder));

    // round N
    sprintf(sPlaceholder, "[%d]", state.nEntered);
    memcpy(screen[2] + 12, sPlaceholder, strlen(sPlaceholder));

    // guessed words
    sprintf(sPlaceholder, "[%d]", state.nGuessed);
    memcpy(screen[10] + 41, sPlaceholder, strlen(sPlaceholder));

    // failed times:
    sprintf(sPlaceholder, "[%d]", state.nFailed);
    memcpy(screen[13] + 38, sPlaceholder, strlen(sPlaceholder));

    // letters entered:
    for( i = 0; i < 27; i++) {
        if (state.lettersEntered[i] == 1) {
            int posX = alphabetPos[i][0];
            int posY = alphabetPos[i][1];
            memset(screen[posX] + posY, ' ', 1);
        }
    }

    // gallows
    for( i = 0 ; i< 23; i++) {
        memcpy(screen[i]+ 63, gallows[state.nFailed][i], strlen(gallows[state.nFailed][i]));
        printf("%s\n", screen[i]);
    }
    printLine();
    fflush(stdout);
}

/*int main(int argc, char const* argv[])             */
/*{                                                  */
/*    [>printWelcome();<]                            */
/*    int i=0;                                       */
/*    for (i = 0; i < 6; i++) {                      */
/*        printGallows(i);                           */
/*    }                                              */
/*    printLevel1();                                 */

/*    static const char * const wordlists[] = {      */
/*        "animals",                                 */
/*        "fruits",                                  */
/*        "instruments",                             */
/*        "passwords",                               */
/*        "programming-languages",                   */
/*        "science",                                 */
/*        "sports",                                  */
/*        "stack-exchange-sites",                    */
/*        NULL                                       */
/*    };                                             */
/*    printCategory((char **)wordlists);             */


/*    User user1 = { "aaa", "aaa", 25};              */
/*    User user2 = { "bbb", "bbb", 50};              */
/*    Ranking rank1[2] = { { 1, user1}, {2, user2} };*/

/*    printScoreboard(rank1, 2);                     */

/*    return 0;                                      */
/*}                                                  */
