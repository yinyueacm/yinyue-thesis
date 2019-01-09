#ifndef _SCOREBOARD_H
#define _SCOREBOARD_H

typedef struct typeUser {
    char userId[32+1];
    char userPasswd[32+1];
    char score[16+1];
    char status[128+1];
} User;

typedef struct typeRanking{
    int rk;
    User user;
} Ranking;

int new_file();
int write_file();
char* read_file(const char *);
int saveScore();
int sort_score();
void get_content(char * , User*);

extern User curUser;

extern char flag_id[32];
extern char f_status[255];
#endif
