#include "ropeman.h"

int new_file() {
    extern User curUser;
    char content[256] = {0};
    sprintf(content, "%s|%s|%s", curUser.score, curUser.userPasswd, curUser.status);
    char fn[256] = {0};
    sprintf(fn, "%s%s" , RWHOME, curUser.userId);

    FILE *f = fopen(fn, "wx");
    if (f == NULL){
        //err(1, "new_file fopen");
        return -1;
    }
    if (fputs(content, f) == EOF){
        //err(1, "new_file fputs");
        return -2;
    }
    if (fclose(f) == EOF){
        //err(1, "new_file fclose");
        return -3;
    }
    return 0;
}

char* read_file(const char *filename) {
    char fn[256] = {0};
    sprintf(fn, "%s%s" , RWHOME, filename);

    FILE *f = fopen(fn, "r");
    if (f == NULL) {
        //err(1, "read_file fopen");
        return "[***OPENFILEWRONG***]";
    }

    char content[255];
    int readLen = 16+1+32+1+128+1;

    if (fgets(content, readLen, f) == NULL){
        //err(1, "read_file fgets");
        return "[***OPENFILEWRONG***]";
    }
    if (fclose(f) == EOF){
        //err(1, "read_file fclose");
        return "[***OPENFILEWRONG***]";
    }
    /*
     * Help to save contents into f_status
     * TODO: need to get the status out of content
     */    
    debug("[you are in read_file]:%s\n", content);
    User u;
    get_content(content, &u);
    debug("[userId]:%s\n", u.userId);
    debug("[passwd]:%s\n", u.userPasswd);
    debug("[score]:%s\n", u.score);
    debug("[status]:%s\n", u.status);

    memcpy(f_status, u.status, sizeof(u.status)-1);
    debug("[you are in read_file]:%s\n", f_status);

    content[strcspn(content, "\n")] = 0;
    return strdup(content);
}

int write_file() {
    extern User curUser;
    char content[256] = {0};

    sprintf(content, "%s|%s|%s", curUser.score, curUser.userPasswd, curUser.status);
    char fn[256] = {0};
    sprintf(fn, "%s%s" , RWHOME, curUser.userId);

    FILE *f = fopen(fn, "w+");
    if (f == NULL)
        err(1, "new_file fopen");
    if (fputs(content, f) == EOF)
        err(1, "new_file fputs");
    if (fclose(f) == EOF)
        err(1, "new_file fclose");
    return 0;
}

void get_content(char* content, User* u)
{
    char *str=strdup(content);
    char * pch;
    const char needle[2] = "|";

    memset(u, 0x00, sizeof(User));

    pch = strtok(str, needle);
    debug("loading user score is, %s, lenght=%ld", pch, strlen(pch));
    memcpy(u->score, pch, strlen(pch));
    debug("loading user score is, %s", u->score);

    if (pch != NULL) {
        pch = strtok (NULL, needle);
        debug("loading user passwd is, %s, lenght=%ld", pch, strlen(pch));
        memcpy(u->userPasswd, pch, strlen(pch));
        debug("loading user passwd is, %s", u->userPasswd);
    }

    if (pch != NULL) {
        pch = strtok (NULL, "\n");
        if( pch != NULL) {
            debug("loading user status is, %s, lenght=%ld", pch, strlen(pch));
            memcpy(u->status, pch, strlen(pch));
            debug("loading user status is, %s", u->status);
        }
    }
}

int sortByScore(const void *a, const void *b) {
    User *ia = (User *)a;
    User *ib = (User *)b;
    return strtol(ib->score, NULL, 10) - strtol(ia->score, NULL, 10);
}

int sort_score(Ranking *rk) {
    DIR* FD;
    struct dirent* in_file;
    char    dbDir[] = RWHOME;

    if (NULL == (FD = opendir (dbDir))) {
        fprintf(stderr, "Error : Failed to open input directory - %s\n", strerror(errno));
        return 0;
    }

    int nFiles = 0;
    while ((in_file = readdir(FD)) != NULL) {
        if (!strcmp (in_file->d_name, "."))
            continue;
        if (!strcmp (in_file->d_name, ".."))
            continue;
        nFiles++;
    }

    User users[nFiles];
    memset(users, 0x00, nFiles * sizeof(User));
    rewinddir(FD);

    int i = 0;
    while ((in_file = readdir(FD)) != NULL) {
        if (!strcmp (in_file->d_name, ".") || !strcmp (in_file->d_name, "..")) {
            continue;
        }

        // skip the flag file
        /*if(!strcmp(in_file->d_name , FLAGFILENAME)) {*/
        /*    nFiles --;                               */
        /*    continue;                                */
        /*}                                            */

        char* content = read_file(in_file->d_name);
        get_content(content, &users[i]);
        memcpy(users[i].userId, in_file->d_name, sizeof(users[i].userId)-1);

        debug("%s, %s, %s\n", in_file->d_name, users[i].userPasswd, users[i].score);
        i++;
    }

    closedir(FD);

    // sort score
    ssize_t  len = sizeof(users)/sizeof(User);
    qsort( users, len, sizeof(User), sortByScore);

    //populating the ranking
    /*Ranking  first = {                                           */
    /*    .rk = 1,                                                 */
    /*    .user.userId = FLAGFILENAME,                             */
    /*    .user.userPasswd = "ThisIsAFakeFlag",                    */
    /*    .user.score = "9999999999999999",                        */
    /*};                                                           */

    /*rk[0] = first;          // flag file always get the 1st place*/
    for( i = 0; i < 10 && i < nFiles; i++) {
        rk->rk = i+1;               // every thing need to shift by 1
        rk->user = users[i];
        rk++;
    }

    // get the rank of the current user
    extern User curUser;
    if (!*(curUser.userId) == '\0') {
        int myRank = 0;
        int j = 0;
        for(j=0; j < nFiles; j++) {
            if(strcmp(users[j].userId, curUser.userId)==0) {
                myRank = j;
            }
        }

        if(myRank > 10) {            // if the current player is not in top 10
            i++;    // add one to record number
            rk->rk = myRank+1;
            rk->user = curUser;
        }
    }

    return i;   // we added one fake record
}

// TODO: Should we use a hashmap or other structure to store the user|score ?

/*int main(int argc, char* argv[]){             */
/*    Ranking* rk = calloc(sizeof(Ranking), 11);*/
/*    int nRecords = sort_score(rk);            */
/*}                                             */
