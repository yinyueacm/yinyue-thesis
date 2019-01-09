#include <stdio.h>
#include <stdlib.h>

void main(){
    int secret, guess;
    char name[32];
    long seed;

    FILE *f = fopen("/dev/urandom", "rb");
    fread(&secret, sizeof(int), 1, f);
    fclose(f);

    printf("Hello! What is your name?\n");
    fgets(name, sizeof(name), stdin);

    printf("Welcome to the guessing number game, ");
    printf(name);
    printf("\nWe generated a random 32-bit number.\nTake a guess and get the password. Good luck.\n");

    printf("Guess a number?\n");
    scanf("%d", &guess);

    if(guess == secret){
        printf("\n");
        printf("Good job! You made it! Here's the flag:\n");
        system("cat flag");
        printf("\n");
    }else{
        printf("Hah! I knew you wouldn't get it.\n");
    }
}

