#include<stdio.h>
#include<string.h>
#include<stdlib.h>

void main(){
    char large_string[256];

    printf("I made it this way to be familiar when you move onto ROP Emporium!\n");
    printf("Please enter a string!!!\n\n>");
    fgets(large_string,256,stdin);

    whoops(&large_string);
}

void whoops(char *str){ //"Whoops! All overflows" -Cap'n Crunch, probably.
    char buffer[16];
    strcpy(buffer,str);
}

void uncalled(){
    printf("\nYour first Buffer Overflow flag!\n");
    exit(0);
}