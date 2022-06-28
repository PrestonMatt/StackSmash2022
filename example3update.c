#include<stdio.h>
#include<string.h>
#include<stdlib.h>

void ohno(void);

void main(){
    printf("Put in your exploit!\n\n");
    printf(">");
    
    ohno();
}

void ohno(){ //"Oh no! I've made a coding error" -Nobody, ever.
    char large_string[64];
    char small_string[16];
    
    fgets(large_string,64,stdin);
    //printf("\nYou put this input in, %s at address %d\n", large_string, &large_string);
    
    printf("Copying memory...%s into a blank buffer...", large_string, small_string);
    memcpy(small_string,large_string,64);
    asm volatile(
        "ret\n\t"
    );
    //We'll use this later
    //strcpy(small_string,large_string);
}