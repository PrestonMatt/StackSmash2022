#include<stdio.h>
#include<string.h>
#include<stdlib.h>

void ohno(char *str);

void main(){
    char large_string[256];

    printf("Put in your exploit!\n\n>");
    fgets(large_string,256,stdin);

    ohno(large_string);
    printf("Try again!\n");
}

void ohno(char *str){ //"Oh no! I've made a coding error" -Nobody, ever.
    char buffer[16];
    memcpy(buffer,str,256);
}