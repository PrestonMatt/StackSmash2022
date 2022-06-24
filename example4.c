#include<stdio.h>
#include<string.h>
#include<stdlib.h>

void mistake(char *str);
void ropGadget1(void);
void ropGadget2(void);
void ropGadget3(void);

void main(){
    char large_string[256];

    printf("Put in your exploit!\n\n>");
    fgets(large_string,256,stdin);

    mistake(large_string);
    printf("Try again!\n");
}

void mistake(char *str){
    char buffer[16];
    memcpy(buffer,str,256);
}

void ropGadget1(){
    asm volatile(
        "push rsp\n\t"
        "ret\n\t"
    );
}

void ropGadget2(){
    asm volatile(
        "pop rax\n\t"
        "ret \n\t"
    );
}

void ropGadget3(){
    asm volatile(
        "jmp rax\n\t"
    );
}