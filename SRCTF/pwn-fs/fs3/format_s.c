#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>

int secret = 0;

int main(int argc, char **argv){
    int *ptr = &secret;
    if(argv[1][0] != 's'){
        printf("Input not accepted!\n");
        return -1;
    }
    printf(argv[1]);
    printf("%c\n", argv[1][0]);

    if (secret == 1337){
        printf("\n");
        printf("Good job! You made it! Here's the flag:\n");
        system("cat flag");
        printf("\n");
    }
    return 0;
}
